from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any
from urllib.request import Request, urlopen


class ToolClient:
    PROTOCOL_VERSION = "2026-07-28"

    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip("/")

    def _request(
        self,
        name: str,
        arguments: dict[str, Any],
        idempotency_key: str,
        dispatch_token: str | None = None,
        dispatch_generation: int | None = None,
    ) -> dict[str, Any]:
        metadata = {
            "io.modelcontextprotocol/clientInfo": {
                "name": "durable-mcp-gateway",
                "version": "1.0.0",
            },
            "io.klavis/idempotencyKey": idempotency_key,
        }
        if dispatch_token is not None:
            metadata["io.klavis/dispatchToken"] = dispatch_token
        if dispatch_generation is not None:
            metadata["io.klavis/dispatchGeneration"] = dispatch_generation
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": idempotency_key,
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments,
                    "_meta": metadata,
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

    def call(
        self,
        name: str,
        arguments: dict[str, Any],
        idempotency_key: str,
        dispatch_token: str,
        dispatch_generation: int,
    ) -> dict[str, Any]:
        return self._request(
            name,
            arguments,
            idempotency_key,
            dispatch_token,
            dispatch_generation,
        )

    @staticmethod
    def request_fingerprint(name: str, arguments: dict[str, Any]) -> str:
        canonical = json.dumps(
            {"name": name, "arguments": arguments},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
        return hashlib.sha256(canonical).hexdigest()

    def lookup(
        self, idempotency_key: str, request_fingerprint: str
    ) -> dict[str, Any]:
        outcome = self._request(
            "lookup_call",
            {
                "idempotency_key": idempotency_key,
                "request_fingerprint": request_fingerprint,
            },
            f"lookup:{uuid.uuid4().hex}",
        )
        return outcome

    def acquire(
        self,
        idempotency_key: str,
        request_fingerprint: str,
        after_revision: int,
    ) -> dict[str, Any]:
        return self._request(
            "acquire_call",
            {
                "idempotency_key": idempotency_key,
                "request_fingerprint": request_fingerprint,
                "after_revision": after_revision,
            },
            f"acquire:{uuid.uuid4().hex}",
        )

    def read_result(self, result_ref: str, result_sha256: str) -> dict[str, Any]:
        return self._request(
            "read_result",
            {
                "result_ref": result_ref,
                "result_sha256": result_sha256,
            },
            f"result:{uuid.uuid4().hex}",
        )

    def release_result(self, result_ref: str, result_sha256: str) -> dict[str, Any]:
        return self._request(
            "release_result",
            {
                "result_ref": result_ref,
                "result_sha256": result_sha256,
            },
            f"release:{uuid.uuid4().hex}",
        )
