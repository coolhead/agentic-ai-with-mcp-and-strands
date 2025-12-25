from mcp.server import FastMCP
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
import threading
import time

# --- MCP Server (same idea as lab) ---
mcp = FastMCP("Calculator Server")

@mcp.tool(description="Add two numbers together")
def add(x: int, y: int) -> int:
    return x + y

@mcp.tool(description="Multiply two numbers together")
def multiply(x: int, y: int) -> int:
    return x * y

def run_server():
    # streamable-http is what the lab uses
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)

# Start server in background thread
t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(1.0)

# --- MCP Client ---
def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

client = MCPClient(create_transport)

with client:
    tools = client.list_tools_sync()
    print("Available MCP tools:", [t["name"] for t in tools])

    # Direct tool calls (no LLM involved)
    r1 = client.call_tool_sync(tool_use_id="proof-1", name="add", arguments={"x": 16, "y": 16})
    print("add(16,16) ->", r1["content"][0]["text"])

    r2 = client.call_tool_sync(tool_use_id="proof-2", name="multiply", arguments={"x": 16, "y": 16})
    print("multiply(16,16) ->", r2["content"][0]["text"])

print("DONE")
