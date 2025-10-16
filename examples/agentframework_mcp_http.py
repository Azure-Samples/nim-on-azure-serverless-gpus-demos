"""Agent Framework + MCP HTTP example with API Key Auth.

Prerequisite:
Start the local MCP server defined in `mcp_server_basic.py` on port 8000:
    python examples/mcp_server_basic.py
"""

import asyncio
import logging
import os

from agent_framework import MCPStreamableHTTPTool
from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv
from rich import print
from rich.logging import RichHandler

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

client = OpenAIResponsesClient(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none",
    model_id=os.environ["NIM_MODEL"],
)


async def main():
    async with MCPStreamableHTTPTool(
        name="hotels", description="Provides tools for hotel search", url="http://localhost:8000/mcp/"
    ) as mcp_server:
        agent = client.create_agent(
            name="Assistant", instructions="Use the tools to achieve the task", tools=mcp_server
        )

        message = (
            "Find me a hotel in San Francisco for 2 nights starting from 2024-01-01."
            "I need a hotel with free WiFi and a pool."
        )
        response = await agent.run(message)
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
