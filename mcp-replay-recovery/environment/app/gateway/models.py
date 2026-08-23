from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Operation:
    session_id: str
    operation_id: str
    schema_version: int
    name: str
    arguments: dict[str, Any]
    depends_on: tuple[str, ...] = ()

    @property
    def logical_id(self) -> str:
        return f"{self.session_id}:{self.operation_id}"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Operation":
        return cls(
            session_id=value["session_id"],
            operation_id=value["operation_id"],
            schema_version=int(value["schema_version"]),
            name=value["name"],
            arguments=dict(value["arguments"]),
            depends_on=tuple(value.get("depends_on", ())),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "operation_id": self.operation_id,
            "schema_version": self.schema_version,
            "name": self.name,
            "arguments": self.arguments,
            "depends_on": list(self.depends_on),
        }

