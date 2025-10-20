"""Agent Framework + Learn MCP server

Prerequisite:
  To send traces to Azure Monitor, set `APPLICATIONINSIGHTS_CONNECTION_STRING` env variable in `.env` file.
"""

import asyncio
import logging
import os

from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.observability import setup_observability
from agent_framework.openai import OpenAIResponsesClient
from dotenv import load_dotenv
from rich import print
from rich.logging import RichHandler

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
setup_observability(enable_sensitive_data=True)

client = OpenAIResponsesClient(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none",
    model_id=os.environ["NIM_MODEL"],
)


async def main():
    async with MCPStreamableHTTPTool(
        name="learn", description="Search documentation from Microsoft Learn", url="https://learn.microsoft.com/api/mcp"
    ) as mcp_server:
        agent = ChatAgent(
            chat_client=client, name="Assistant", instructions="Use the tools to achieve the task", tools=mcp_server
        )

        message = "Does Azure offer serverless GPUs?"
        response = await agent.run(message)
        print("Response: ", response.text)


if __name__ == "__main__":
    asyncio.run(main())
