from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("Starting agent...")
    try:
        agent = Agent(
            name="SimpleAssistant",
            instructions="Answer general knowledge questions.",
            model="gpt-4o-mini"
        )

        message = "What is the capital of France?"
        print(f"\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    print("Started Running...")
    asyncio.run(main())