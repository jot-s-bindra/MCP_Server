from agents import Agent, Runner, trace, gen_trace_id
from agents.mcp import MCPServer, MCPServerStdio
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant and would use given tools to help the user.",
        mcp_servers=[mcp_server],
    )

    message = "What's the weather in New Delhi ?"
    response = await Runner.run(agent, message)
    print(response.final_output)

async def main():
    try:
        async with MCPServerStdio(
            name="Weather Server",
            params={
                "command": "python",
                "args": ["server.py"]
            },
            cache_tools_list=True,
        ) as server:
            tool_list = await server.list_tools()
            for tool in tool_list:
                print(f"Tool Name: {tool.name}")

            trace_id = gen_trace_id()
            print(f"Trace ID: {trace_id}")
            with trace(workflow_name="Weather Service Example", trace_id=trace_id):
                print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")

            print("Starting MCP server")
            await run(server)
    except Exception as e:
        print(f"Failed to connect to MCP server: {e}")

if __name__ == "__main__":
    asyncio.run(main())