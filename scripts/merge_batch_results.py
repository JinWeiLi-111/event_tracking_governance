import argparse
import json
import re
from pathlib import Path


def batch_index(path: Path) -> int:
    match = re.search(r"batch(\d+)_review\.json$", path.name)
    if not match:
        return 10**9
    return int(match.group(1))


def merge_batch_results(input_dir: Path, output_file: Path) -> None:
    batch_files = sorted(input_dir.glob("batch*_review.json"), key=batch_index)
    if not batch_files:
        raise FileNotFoundError(f"No batch review files found in: {input_dir}")

    merged_items = []
    merged_batches = []

    for file_path in batch_files:
        with file_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        batch_id = str(payload.get("batch_id", ""))
        items = payload.get("items", [])
        if not isinstance(items, list):
            raise ValueError(f"`items` is not a list in file: {file_path}")

        merged_batches.append(batch_id)
        merged_items.extend(items)

    merged_payload = {
        "status": "completed",
        "source_batches": merged_batches,
        "total_items": len(merged_items),
        "items": merged_items,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(merged_payload, f, ensure_ascii=False, indent=2)

    print(f"Merged {len(batch_files)} files into: {output_file}")
    print(f"Total items: {len(merged_items)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge items from batch*_review.json into one JSON file."
    )
    parser.add_argument(
        "--input-dir",
        default="workspace/turn_2/agent_b_review",
        help="Directory containing batch*_review.json files.",
    )
    parser.add_argument(
        "--output-file",
        default="workspace/turn_2/final/all_batches_result.json",
        help="Output merged JSON file path.",
    )
    args = parser.parse_args()

    merge_batch_results(Path(args.input_dir), Path(args.output_file))


if __name__ == "__main__":
    main()
