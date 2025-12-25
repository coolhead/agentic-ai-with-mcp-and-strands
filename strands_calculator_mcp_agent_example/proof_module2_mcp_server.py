from mcp.server import FastMCP

mcp = FastMCP("Calculator Server")

@mcp.tool(description="Add two numbers together")
def add(x: int, y: int) -> int:
    return x + y

@mcp.tool(description="Multiply two numbers together")
def multiply(x: int, y: int) -> int:
    return x * y

print("Starting MCP Calculator Server on http://localhost:8000")
mcp.run(transport="streamable-http")
