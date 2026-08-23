from __future__ import annotations

import os


_hits: dict[str, int] = {}


def hit(point: str) -> None:
    configured = os.environ.get("FAULT_POINT")
    if configured != point:
        return
    _hits[point] = _hits.get(point, 0) + 1
    after = int(os.environ.get("FAULT_AFTER", "1"))
    if _hits[point] == after:
        os._exit(86)

