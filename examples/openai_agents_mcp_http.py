"""OpenAI Agents framework + MCP HTTP example.

Prerequisite:
Start the local MCP server defined in `mcp_server_basic.py` on port 8000:
    python examples/mcp_server_basic.py
"""

import asyncio
import logging
import os

import openai
from agents import Agent, OpenAIResponsesModel, Runner, set_tracing_disabled
from agents.mcp.server import MCPServerStreamableHttp
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)
# Disable tracing since we're not connected to a supported tracing provider
set_tracing_disabled(disabled=True)

# Setup the OpenAI client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)

client = openai.AsyncOpenAI(base_url=os.environ["NIM_ENDPOINT"], api_key="none")
MODEL_NAME = os.environ["NIM_MODEL"]

mcp_server = MCPServerStreamableHttp(name="weather", params={"url": "http://localhost:8000/mcp/"})

agent = Agent(
    name="Assistant",
    instructions="Use the tools to achieve the task",
    mcp_servers=[mcp_server],
    model=OpenAIResponsesModel(model=MODEL_NAME, openai_client=client)
)


async def main():
    await mcp_server.connect()
    message = "Find me a hotel in San Francisco for 2 nights starting from 2024-01-01. I need a hotel with free WiFi and a pool."
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
    await mcp_server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
