"""PydanticAI + MCP HTTP example.

Prerequisite:
Start the local MCP server defined in `mcp_server_basic.py` on port 8000:
    python examples/mcp_server_basic.py
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider

# Setup the OpenAI client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)

client = AsyncOpenAI(base_url=os.environ["NIM_ENDPOINT"], api_key="none")

model = OpenAIResponsesModel(
    os.environ["NIM_MODEL"],
    provider=OpenAIProvider(openai_client=client),
    profile=OpenAIModelProfile(openai_responses_requires_function_call_status_none=True),
)

server = MCPServerStreamableHTTP(url="http://localhost:8000/mcp")

agent: Agent[None, str] = Agent(
    model,
    system_prompt="You are a travel planning agent. You can help users find hotels.",
    toolsets=[server],
)


async def main():
    result = await agent.run(
        "Find me a hotel in San Francisco for 2 nights starting from 2024-01-01. I need free WiFi and a pool."
    )
    print(result.output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
