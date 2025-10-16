import asyncio
import logging
import os

import openai
from agents import Agent, OpenAIResponsesModel, Runner, set_tracing_disabled
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)
# Disable tracing since we're not connected to a supported tracing provider
set_tracing_disabled(disabled=True)

load_dotenv(override=True)
client = openai.AsyncOpenAI(base_url=os.environ["NIM_ENDPOINT"], api_key="none")
MODEL_NAME = os.environ["NIM_MODEL"]

agent = Agent(
    name="Spanish tutor",
    instructions="You are a Spanish tutor. Help the user learn Spanish. ONLY respond in Spanish.",
    model=OpenAIResponsesModel(model=MODEL_NAME, openai_client=client),
)


async def main():
    result = await Runner.run(agent, input="hi how are you?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
