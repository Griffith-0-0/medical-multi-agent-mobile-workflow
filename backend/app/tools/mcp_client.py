import os
from typing import Any, Dict

import httpx


def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp")

    response = httpx.post(
        mcp_url,
        json={
            "jsonrpc": "2.0",
            "id": "medical-care-tool-call",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        },
        timeout=10,
    )
    response.raise_for_status()

    payload = response.json()
    if "error" in payload:
        raise RuntimeError(payload["error"]["message"])

    content = payload.get("result", {}).get("content", [])
    if not content:
        raise RuntimeError("Reponse MCP vide")

    return content[0].get("text", "")
