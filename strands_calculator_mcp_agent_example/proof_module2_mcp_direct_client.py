from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

client = MCPClient(create_transport)

with client:
    tools = client.list_tools_sync()
    print("Available MCP tools:", [t["name"] for t in tools])

    r1 = client.call_tool_sync(
        tool_use_id="proof-1",
        name="add",
        arguments={"x": 16, "y": 16},
    )
    print("add(16,16) ->", r1["content"][0]["text"])

    r2 = client.call_tool_sync(
        tool_use_id="proof-2",
        name="multiply",
        arguments={"x": 16, "y": 16},
    )
    print("multiply(16,16) ->", r2["content"][0]["text"])

print("DONE")
