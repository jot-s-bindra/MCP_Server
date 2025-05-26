from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerSse
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def run(mcp_server: MCPServer):
    try:
        agent = Agent(
            name="Assistant",
            instructions="Use the Weather Server to fetch weather data for user queries.",
            mcp_servers=[mcp_server],
            model="gpt-4o-mini"  # Changed from o3-mini
        )

        message = "How is the weather in Hyderabad?"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
    except Exception as e:
        print(f"Error running agent: {e}")

async def main():
    print("Starting MCP server...")
    try:
        async with MCPServerSse(
            name="Custom SSE server",
            params={
                "url": "http://localhost:8000/sse",
            },
            cache_tools_list=True,
        ) as server:
            tool_list = await server.list_tools()
            for tool in tool_list:
                print(f"Tool: {tool.name}")

            trace_id = gen_trace_id()
            print(f"Trace ID: {trace_id}")
            with trace(workflow_name="Weather SSE Example", trace_id=trace_id):
                print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
                await run(server)
    except Exception as e:
        print(f"Failed to connect to MCP server: {e}")

if __name__ == "__main__":
    print("Started Running...")
    asyncio.run(main())