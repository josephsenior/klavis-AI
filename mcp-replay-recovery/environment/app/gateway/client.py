from __future__ import annotations

import json
from typing import Any
from urllib.request import Request, urlopen


class ToolClient:
    PROTOCOL_VERSION = "2026-07-28"

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
                    "_meta": {
                        "io.modelcontextprotocol/clientInfo": {
                            "name": "durable-mcp-gateway",
                            "version": "1.0.0",
                        },
                        "io.klavis/idempotencyKey": idempotency_key,
                    },
                },
            }
        ).encode()
        request = Request(
            f"{self.endpoint}/mcp",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": self.PROTOCOL_VERSION,
                "Mcp-Method": "tools/call",
                "Mcp-Name": name,
            },
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            message = json.load(response)
        if "error" in message:
            raise RuntimeError(message["error"]["message"])
        result = message["result"]
        if result.get("isError"):
            content = result.get("content", [])
            detail = content[0].get("text", "tool call failed") if content else "tool call failed"
            raise RuntimeError(detail)
        return dict(result["structuredContent"])
