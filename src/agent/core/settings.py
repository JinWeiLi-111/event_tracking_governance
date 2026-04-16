from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing_extensions import runtime


@dataclass(slots=True)
class RuleConfig:
    name: str
    enabled: bool = True
    params: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class AgentSettings:
    domain: str
    output_dir: str
    rule_configs: list[RuleConfig] = field(default_factory=list)
    default_values: dict[str, object] = field(default_factory=dict)
    required_fields: list[str] = field(default_factory=list)

    @classmethod
    def from_json_file(cls, file_path: Path) -> "AgentSettings":
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        rule_configs = [
            RuleConfig(
                name=item["name"],
                enabled=item.get("enabled", True),
                params=item.get("params", {}),
            )
            for item in payload.get("rule_configs", [])
        ]
        return cls(
            domain=payload.get("domain", "boss_zhipin"),
            output_dir=payload.get("output_dir", "output"),
            rule_configs=rule_configs,
            default_values=payload.get("default_values", {}),
            required_fields=payload.get("required_fields", []),
        )
        