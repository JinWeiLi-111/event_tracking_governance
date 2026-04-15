from __future__ import annotations

import argparse
from pathlib import Path

from agent.core.settings import AgentSettings
from agent.services.metadata_completion import MetadataCompletionService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="agent-cli",
        description="Complete legacy tracking metadata with configurable rules.",
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to agent config JSON file.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to legacy events metadata JSON file.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path for completed metadata JSON.",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Optional output path for audit report JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = AgentSettings.from_json_file(Path(args.config))
    service = MetadataCompletionService(settings=settings)

    result = service.run(
        input_path=Path(args.input),
        output_path=Path(args.output) if args.output else None,
        report_path=Path(args.report) if args.report else None,
    )
    print(
        f"Processed {result.total_events} events; "
        f"completed {result.completed_events}; "
        f"warnings {result.warning_count}."
    )


if __name__ == "__main__":
    main()
