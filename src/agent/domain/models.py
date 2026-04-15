from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EventMetadata:
    event_name: str
    event_description: str | None = None
    properties: dict[str, object] = field(default_factory=dict)
    required_properties: list[str] = field(default_factory=list)
    owner: str | None = None
    source_platform: str | None = None
    data_sensitivity: str | None = None
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "EventMetadata":
        return cls(
            event_name=str(payload.get("event_name", "")).strip(),
            event_description=payload.get("event_description"),  # type: ignore[arg-type]
            properties=dict(payload.get("properties", {})),  # type: ignore[arg-type]
            required_properties=list(payload.get("required_properties", [])),  # type: ignore[arg-type]
            owner=payload.get("owner"),  # type: ignore[arg-type]
            source_platform=payload.get("source_platform"),  # type: ignore[arg-type]
            data_sensitivity=payload.get("data_sensitivity"),  # type: ignore[arg-type]
            tags=list(payload.get("tags", [])),  # type: ignore[arg-type]
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "event_name": self.event_name,
            "event_description": self.event_description,
            "properties": self.properties,
            "required_properties": self.required_properties,
            "owner": self.owner,
            "source_platform": self.source_platform,
            "data_sensitivity": self.data_sensitivity,
            "tags": self.tags,
        }


@dataclass(slots=True)
class RuleWarning:
    event_name: str
    rule_name: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "rule_name": self.rule_name,
            "message": self.message,
        }


@dataclass(slots=True)
class CompletionStats:
    total_events: int
    completed_events: int
    warning_count: int
