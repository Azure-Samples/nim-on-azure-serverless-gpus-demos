import asyncio
import os
import logging

from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv
from rich import print

load_dotenv(override=True)
logging.basicConfig(level=logging.DEBUG)

client = OpenAIResponsesClient(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none",
    model_id=os.environ["NIM_MODEL"],
)

async def main():
    response = await client.get_response("Whats weather today in San Francisco?")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
