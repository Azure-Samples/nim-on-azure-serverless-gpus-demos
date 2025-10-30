import asyncio
import logging
import os
import random
from datetime import datetime
from typing import Annotated

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider
from rich.logging import RichHandler

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = AsyncOpenAI(base_url=os.environ["NIM_ENDPOINT"], api_key="none")

model = OpenAIResponsesModel(
    os.environ["NIM_MODEL"],
    provider=OpenAIProvider(openai_client=client),
    profile=OpenAIModelProfile(
        openai_responses_requires_function_call_status_none=True,
        openai_supports_tool_choice_required=False,
    ),
)


# ----------------------------------------------------------------------------------
# Sub-agent 1 tools: weekend planning
# ----------------------------------------------------------------------------------


def get_weather(
    city: Annotated[str, Field(description="The city to get the weather for.")],
    date: Annotated[str, Field(description="The date to get weather for in format YYYY-MM-DD.")],
) -> dict:
    """Returns weather data for a given city and date."""
    logger.info(f"Getting weather for {city} on {date}")
    # deterministic-ish mock
    if random.random() < 0.05:
        return {"temperature": 72, "description": "Sunny"}
    else:
        return {"temperature": 60, "description": "Rainy"}


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
    """Gets the current date from the system (YYYY-MM-DD)."""
    logger.info("Getting current date")
    return datetime.now().strftime("%Y-%m-%d")


weekend_agent = Agent(
    model,
    tools=[get_weather, get_activities, get_current_date],
    system_prompt=(
        "You help users plan their weekends and choose the best activities for the given weather. "
        "If an activity would be unpleasant in the weather, don't suggest it. "
        "Include the date of the weekend in your response."
    ),
)


async def plan_weekend(ctx: RunContext[None], query: str) -> str:
    """Plan a weekend based on user query and return the final response."""
    logger.info("Tool: plan_weekend invoked")
    res = await weekend_agent.run(query)
    return res.output


# ----------------------------------------------------------------------------------
# Sub-agent 2 tools: meal planning
# ----------------------------------------------------------------------------------


def find_recipes(query: Annotated[str, Field(description="User query or desired meal/ingredient")]) -> list[dict]:
    """Returns recipes (JSON) based on a query."""
    logger.info(f"Finding recipes for '{query}'")
    if "pasta" in query.lower():
        recipes = [
            {
                "title": "Pasta Primavera",
                "ingredients": ["pasta", "vegetables", "olive oil"],
                "steps": ["Cook pasta.", "Sauté vegetables."],
            }
        ]
    elif "tofu" in query.lower():
        recipes = [
            {
                "title": "Tofu Stir Fry",
                "ingredients": ["tofu", "soy sauce", "vegetables"],
                "steps": ["Cube tofu.", "Stir fry veggies."],
            }
        ]
    else:
        recipes = [
            {
                "title": "Grilled Cheese Sandwich",
                "ingredients": ["bread", "cheese", "butter"],
                "steps": ["Butter bread.", "Place cheese between slices.", "Grill until golden brown."],
            }
        ]
    return recipes


def check_fridge() -> list[str]:
    """Returns a JSON list of ingredients currently in the fridge."""
    logger.info("Checking fridge for current ingredients")
    if random.random() < 0.5:
        items = ["pasta", "tomato sauce", "bell peppers", "olive oil"]
    else:
        items = ["tofu", "soy sauce", "broccoli", "carrots"]
    return items


meal_agent = Agent(
    model,
    tools=[find_recipes, check_fridge],
    system_prompt=(
        "You help users plan meals and choose the best recipes. "
        "Include the ingredients and cooking instructions in your response. "
        "Indicate what the user needs to buy from the store when their fridge is missing ingredients."
    ),
)


async def plan_meal(ctx: RunContext[None], query: str) -> str:
    """Plan a meal based on user query and return the final response."""
    logger.info("Tool: plan_meal invoked")
    res = await meal_agent.run(query)
    return res.output


# ----------------------------------------------------------------------------------
# Supervisor agent orchestrating sub-agents
# ----------------------------------------------------------------------------------

supervisor_agent = Agent(
    model,
    system_prompt=(
        "You are a supervisor managing two specialist agents: a weekend planning agent and a meal planning agent. "
        "Break down the user's request, decide which specialist (or both) to call via the available tools, "
        "and then synthesize a final helpful answer. When invoking a tool, provide clear, concise queries."
    ),
    tools=[plan_weekend, plan_meal],
)


async def main():
    user_query = "my kids want pasta for dinner and i need a recipe"
    result = await supervisor_agent.run(user_query)
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
