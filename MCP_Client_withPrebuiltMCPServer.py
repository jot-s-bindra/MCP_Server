from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def run(file_mcp_server, time_mcp_server):
    try:
        agent = Agent(
            name="Assistant",
            instructions="Use the FileSystem server to read user data and the Time server for time zone calculations.",
            mcp_servers=[file_mcp_server, time_mcp_server],
            model="gpt-4o-mini" 
        )

        # Query 1: Song suggestion
        message = "Look at my favorite songs. Suggest one new song that I might like"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)

        # Query 2: Time zone conversion
        message = "When it's 4 PM in New York, what time is it in London?"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
    except Exception as e:
        print(f"Error running agent: {e}")

async def main():
    print("Starting MCP servers...")
    try:
        async with MCPServerStdio(
            name="FileSystem server",
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "sample_files"]
            },
            cache_tools_list=True,
        ) as file_mcp_server, MCPServerStdio(
            name="Time server",
            params={
                "command": "python",
                "args": ["-m", "mcp_server_time", "--local-timezone=America/New_York"]
            },
            cache_tools_list=True,
        ) as time_mcp_server:
            # List tools for debugging
            for server, name in [(file_mcp_server, "FileSystem server"), (time_mcp_server, "Time server")]:
                tools = await server.list_tools()
                print(f"\nTools for {name}:")
                for tool in tools:
                    print(f"  - {tool.name}")

            # Add tracing
            trace_id = gen_trace_id()
            print(f"\nTrace ID: {trace_id}")
            with trace(workflow_name="File and Time Example", trace_id=trace_id):
                print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
                await run(file_mcp_server, time_mcp_server)
    except Exception as e:
        print(f"Failed to start MCP servers: {e}")

if __name__ == "__main__":
    print("Started Running...")
    asyncio.run(main())