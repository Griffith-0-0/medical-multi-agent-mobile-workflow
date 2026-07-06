import os
from typing import Any

import anyio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def _call_mcp_tool_async(tool_name: str, arguments: dict[str, Any]) -> str:
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp")

    async with streamablehttp_client(mcp_url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)

    if not result.content:
        raise RuntimeError("Reponse MCP vide")

    first_content = result.content[0]
    text = getattr(first_content, "text", None)
    if not text:
        raise RuntimeError("Reponse MCP non textuelle")

    return text


def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> str:
    return anyio.run(_call_mcp_tool_async, tool_name, arguments)
