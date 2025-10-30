import asyncio
import logging
import os
import random
from datetime import datetime

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider
from rich.logging import RichHandler

load_dotenv(override=True)
logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger(__name__)

client = AsyncOpenAI(base_url=os.environ["NIM_ENDPOINT"], api_key="none")

model = OpenAIResponsesModel(
    os.environ["NIM_MODEL"],
    provider=OpenAIProvider(openai_client=client),
    profile=OpenAIModelProfile(
        openai_responses_requires_function_call_status_none=True, openai_supports_tool_choice_required=False
    ),
)


def get_weather(city: str) -> dict:
    """Returns weather data for a given city, a dictionary with temperature and description."""
    logger.info(f"Getting weather for {city}")
    if random.random() < 0.05:
        return {
            "city": city,
            "temperature": 72,
            "description": "Sunny",
        }
    else:
        return {
            "city": city,
            "temperature": 60,
            "description": "Rainy",
        }


def get_activities(city: str, date: str) -> list:
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


agent = Agent(
    model,
    system_prompt=(
        "You help users plan their weekends and choose the best activities for the given weather."
        "If an activity would be unpleasant in the weather, don't suggest it."
        "Include the date of the weekend in your response."
    ),
    tools=[get_weather, get_activities, get_current_date],
)


async def main():
    result = await agent.run("what can I do for funzies this weekend in Seattle?")
    print(result.output)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    asyncio.run(main())
