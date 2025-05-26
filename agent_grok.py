from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

agent = Agent(
    name="PoemWritter",
    instructions="You are a helpful assistant that writes poems.",
    model=OpenAIChatCompletionsModel(
        model="llama-3.1-8b-instant",
        openai_client=client
    )
)

result = Runner.run_sync(agent, "Write a poem about a cat.")
print(result.final_output)