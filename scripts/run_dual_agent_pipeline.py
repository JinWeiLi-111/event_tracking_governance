#!/usr/bin/env python3
"""Utility script for dual-agent governance pipeline.

Subcommands:
1) bootstrap: copy batch input files into workspace/input.
2) check: verify batch coverage across input/A/B folders.
3) finalize: build final batch*_result.json from Agent B verdict files.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


BASE_FIELDS = [
    "埋点id",
    "页面位置",
    "功能名称",
    "事件类型",
    "埋点中文名",
    "埋点英文名",
    "埋点描述",
]

BATCH_PATTERNS = [
    re.compile(r"batch(?P<id>\d+)_report\.json$"),
    re.compile(r"batch(?P<id>\d+)_input\.json$"),
    re.compile(r"batch(?P<id>\d+)_governed\.json$"),
    re.compile(r"batch(?P<id>\d+)_review\.json$"),
    re.compile(r"batch(?P<id>\d+)_result\.json$"),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def detect_batch_id(path: Path, payload: dict) -> str:
    batch_id = payload.get("batch_id")
    if batch_id is not None and str(batch_id).strip():
        return str(batch_id).strip()

    for pattern in BATCH_PATTERNS:
        match = pattern.search(path.name)
        if match:
            return match.group("id")
    return "unknown"


def iter_json_files(folder: Path) -> Iterable[Path]:
    if not folder.exists():
        return []
    return sorted(p for p in folder.glob("*.json") if p.is_file())


def extract_items(payload) -> List[dict]:
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return [x for x in payload["items"] if isinstance(x, dict)]
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        return [payload]
    return []


def parse_batch_file(path: Path) -> Tuple[str, List[dict]]:
    payload = load_json(path)
    if isinstance(payload, dict):
        batch_id = detect_batch_id(path, payload)
    else:
        batch_id = detect_batch_id(path, {})
    return batch_id, extract_items(payload)


def discover_batches(folder: Path) -> Dict[str, Path]:
    result: Dict[str, Path] = {}
    for file_path in iter_json_files(folder):
        try:
            batch_id, _ = parse_batch_file(file_path)
        except Exception:
            continue
        if batch_id == "unknown":
            continue
        result[batch_id] = file_path
    return result


def normalize_completed_fields(record: dict) -> dict:
    """Try to pull final 7 base fields from various structures."""
    for key in ("validated_output", "governed_output", "completed_fields"):
        value = record.get(key)
        if isinstance(value, dict):
            return {k: value.get(k, "NULL") for k in BASE_FIELDS}

    # Fall back: record itself may already be completed fields.
    if all(field in record for field in BASE_FIELDS):
        return {k: record.get(k, "NULL") for k in BASE_FIELDS}

    return {}


def cmd_bootstrap(args: argparse.Namespace) -> int:
    source_dir = Path(args.source_dir)
    target_dir = Path(args.target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    candidates = sorted(source_dir.glob("batch*_report.json"))
    if not candidates:
        print(f"[bootstrap] no batch*_report.json found in {source_dir}")
        return 1

    copied = 0
    for src in candidates:
        match = re.search(r"batch(\d+)_report\.json$", src.name)
        if not match:
            continue
        batch_id = match.group(1)
        dst = target_dir / f"batch{batch_id}_input.json"
        if dst.exists() and not args.overwrite:
            print(f"[bootstrap] skip existing: {dst}")
            continue
        shutil.copy2(src, dst)
        copied += 1
        print(f"[bootstrap] copied {src.name} -> {dst.name}")

    print(f"[bootstrap] copied files: {copied}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    input_batches = discover_batches(Path(args.input_dir))
    a_batches = discover_batches(Path(args.agent_a_dir))
    b_batches = discover_batches(Path(args.agent_b_dir))

    all_ids = sorted(
        set(input_batches.keys()) | set(a_batches.keys()) | set(b_batches.keys()),
        key=lambda x: (x == "unknown", int(x) if x.isdigit() else 10**9),
    )

    if not all_ids:
        print("[check] no batch files detected.")
        return 1

    print("batch_id\tinput\tagent_a\tagent_b\tinput_items\ta_items\tb_items")
    missing = 0
    for bid in all_ids:
        in_file = input_batches.get(bid)
        a_file = a_batches.get(bid)
        b_file = b_batches.get(bid)
        in_n = len(parse_batch_file(in_file)[1]) if in_file else 0
        a_n = len(parse_batch_file(a_file)[1]) if a_file else 0
        b_n = len(parse_batch_file(b_file)[1]) if b_file else 0

        if not in_file or not a_file or not b_file:
            missing += 1

        print(
            f"{bid}\t"
            f"{'Y' if in_file else 'N'}\t"
            f"{'Y' if a_file else 'N'}\t"
            f"{'Y' if b_file else 'N'}\t"
            f"{in_n}\t{a_n}\t{b_n}"
        )

    if missing:
        print(f"[check] batches with missing stage files: {missing}")
        return 2
    print("[check] all batches have input + agent_a + agent_b files.")
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:
    review_dir = Path(args.agent_b_dir)
    final_dir = Path(args.final_dir)
    fail_dir = Path(args.fail_dir)
    final_dir.mkdir(parents=True, exist_ok=True)
    fail_dir.mkdir(parents=True, exist_ok=True)

    review_files = sorted(review_dir.glob("batch*_review.json"))
    if not review_files:
        print(f"[finalize] no review files found in {review_dir}")
        return 1

    allow = {"PASS"}
    if args.allow_warn:
        allow.add("WARN")

    total_fail = 0
    for review_file in review_files:
        batch_id, records = parse_batch_file(review_file)
        pass_items: List[dict] = []
        fail_items: List[dict] = []

        for record in records:
            verdict = str(record.get("verdict", "")).upper().strip()
            normalized = normalize_completed_fields(record)

            if verdict in allow and normalized:
                pass_items.append(normalized)
                continue

            if verdict:
                fail_items.append(
                    {
                        "record_id": record.get("record_id", "unknown"),
                        "verdict": verdict,
                        "violations": record.get("violations", []),
                    }
                )
            else:
                fail_items.append(
                    {
                        "record_id": record.get("record_id", "unknown"),
                        "verdict": "UNKNOWN",
                        "violations": [{"reason": "Missing verdict or invalid format"}],
                    }
                )

        final_payload = {
            "batch_id": batch_id,
            "items": pass_items,
            "meta": {
                "source_review_file": review_file.name,
                "total_records": len(records),
                "pass_records": len(pass_items),
                "failed_records": len(fail_items),
                "allow_warn": args.allow_warn,
            },
        }
        fail_payload = {
            "batch_id": batch_id,
            "source_review_file": review_file.name,
            "failed_records": fail_items,
        }

        final_path = final_dir / f"batch{batch_id}_result.json"
        fail_path = fail_dir / f"batch{batch_id}_failures.json"
        dump_json(final_path, final_payload)
        dump_json(fail_path, fail_payload)

        total_fail += len(fail_items)
        print(
            f"[finalize] batch{batch_id}: pass={len(pass_items)}, "
            f"fail={len(fail_items)} -> {final_path.name}"
        )

    if total_fail and args.strict_fail:
        print(f"[finalize] blocked: total failed records={total_fail}")
        return 3

    print(f"[finalize] completed. total failed records={total_fail}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run dual-agent governance pipeline helpers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_bootstrap = subparsers.add_parser(
        "bootstrap",
        help="Copy batch*_report.json to workspace/input as batch*_input.json.",
    )
    p_bootstrap.add_argument("--source-dir", default="orgin_input")
    p_bootstrap.add_argument("--target-dir", default="workspace/input")
    p_bootstrap.add_argument("--overwrite", action="store_true")
    p_bootstrap.set_defaults(func=cmd_bootstrap)

    p_check = subparsers.add_parser(
        "check",
        help="Check whether input/A/B files exist for each batch.",
    )
    p_check.add_argument("--input-dir", default="workspace/input")
    p_check.add_argument("--agent-a-dir", default="workspace/agent_a_output")
    p_check.add_argument("--agent-b-dir", default="workspace/agent_b_review")
    p_check.set_defaults(func=cmd_check)

    p_finalize = subparsers.add_parser(
        "finalize",
        help="Generate final batch results from Agent B review files.",
    )
    p_finalize.add_argument("--agent-b-dir", default="workspace/agent_b_review")
    p_finalize.add_argument("--final-dir", default="workspace/final")
    p_finalize.add_argument("--fail-dir", default="workspace/agent_b_review")
    p_finalize.add_argument("--allow-warn", action="store_true")
    p_finalize.add_argument("--strict-fail", action="store_true", default=True)
    p_finalize.add_argument("--no-strict-fail", dest="strict_fail", action="store_false")
    p_finalize.set_defaults(func=cmd_finalize)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
