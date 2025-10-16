import asyncio
import logging
import os
import random
from datetime import datetime
from typing import Annotated

from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv
from pydantic import Field
from rich import print
from rich.logging import RichHandler

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("weekend_assistant")

client = OpenAIResponsesClient(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none",
    model_id=os.environ["NIM_MODEL"],
)


def get_weather(
    city: Annotated[str, Field(description="The city to get the weather for.")],
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


def get_activities(
    city: Annotated[str, Field(description="The city to get activities for.")],
    date: Annotated[str, Field(description="The date to get activities for in format YYYY-MM-DD.")],
) -> list[dict]:
    """Returns a list of activities for a given city and date."""
    logger.info(f"Getting activities for {city} on {date}")
    return [
        {"name": "Hiking", "location": city},
        {"name": "Beach", "location": city},
        {"name": "Museum", "location": city},
    ]


def get_current_date() -> str:
    """Gets the current date from the system and returns as a string in format YYYY-MM-DD."""
    logger.info("Getting current date")
    return datetime.now().strftime("%Y-%m-%d")


agent = client.create_agent(
    instructions=(
        "You help users plan their weekends and choose the best activities for the given weather. "
        "If an activity would be unpleasant in weather, don't suggest it. Include date of the weekend in response."
    ),
    tools=[get_weather, get_activities, get_current_date],
)


async def main():
    response = await agent.run("hii what can I do this weekend in San Francisco?")
    print(response.text)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    asyncio.run(main())
