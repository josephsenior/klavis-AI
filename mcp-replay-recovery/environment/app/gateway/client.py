from __future__ import annotations

import json
from typing import Any
from urllib.request import Request, urlopen


class ToolClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip("/")

    def call(self, name: str, arguments: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": idempotency_key,
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments,
                    "_meta": {"idempotency_key": idempotency_key},
                },
            }
        ).encode()
        request = Request(
            f"{self.endpoint}/rpc",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            message = json.load(response)
        if "error" in message:
            raise RuntimeError(message["error"]["message"])
        return dict(message["result"])

