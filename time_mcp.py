from datetime import datetime
from fastmcp import FastMCP


mcp = FastMCP("Time Server")

@mcp.tool(description="Returns current date in format YYYY-MM-DD.")
def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

@mcp.tool(description="Returns current date and time in ISO 8601 YYYY-MM-DDTHH:MM:SS.")
def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)