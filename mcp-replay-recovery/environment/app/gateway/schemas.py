from __future__ import annotations

from typing import Any

from .models import Operation


def current_wire_call(operation: Operation) -> tuple[str, dict[str, Any]]:
    """Return the v2 wire call for a persisted operation."""
    return operation.name, dict(operation.arguments)
