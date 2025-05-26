from mcp.server.fastmcp import FastMCP
import requests

# Create server
mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(city: str) -> str:
    """Fetches weather for a given city."""
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}", params={"format": "j1"})  
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching weather for {city}: {str(e)}"

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")