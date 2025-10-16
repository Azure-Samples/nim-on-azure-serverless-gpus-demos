import asyncio
import logging
import os
import random
from typing import Annotated

from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv
from pydantic import Field
from rich import print
from rich.logging import RichHandler


load_dotenv(override=True)

# Setup logging with rich
logging.basicConfig(level=logging.DEBUG, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("weekend_planner")

client = OpenAIResponsesClient(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none",
    model_id=os.environ["NIM_MODEL"],
)


def get_weather(
    city: Annotated[str, Field(description="City name, spelled out fully")],
) -> dict:
    """Returns weather data for a given city, a dictionary with temperature and description."""
    logger.info(f"Getting weather for {city}")
    if random.random() < 0.05:
        return {
            "temperature": 72,
            "description": "Sunny",
        }
    else:
        return {
            "temperature": 60,
            "description": "Rainy",
        }


agent = client.create_agent(
    instructions="You're an informational agent. Answer questions cheerfully.", tools=[get_weather]
)


async def main():
    response = await agent.run("how's weather today in sf?")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())