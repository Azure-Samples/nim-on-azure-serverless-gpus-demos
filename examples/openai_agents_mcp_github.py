"""OpenAI Agents framework + GitHub MCP server example for issue triaging.

This script demonstrates how to use the OpenAI Agents SDK with the GitHub MCP
server to triage stale issues in a repository.
"""

import asyncio
import logging
import os

import openai
from agents import Agent, OpenAIResponsesModel, Runner, set_tracing_disabled
from agents.mcp import create_static_tool_filter
from agents.mcp.server import MCPServerStreamableHttp
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich import print

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("issue_labeler")

# Disable tracing since we're not connected to a supported tracing provider
set_tracing_disabled(disabled=True)

load_dotenv(override=True)

client = openai.AsyncOpenAI(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none",
)
MODEL_NAME = os.environ["NIM_MODEL"]


# Setup GitHub MCP server
mcp_server = MCPServerStreamableHttp(
    name="github",
    params={
        "url": "https://api.githubcopilot.com/mcp/",
        "headers": {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
    },
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["get_issue", "search_code", "search_issues", "list_label"]
    ),
)


class LabelOutput(BaseModel):
    url: str = Field(description="URL of the issue")
    title: str = Field(description="Title of the issue")
    label: str = Field(description="Label to apply to the issue")
    reasoning: str = Field(description="Reasoning behind the label decision")


agent = Agent(
    name="Issue Labeler",
    mcp_servers=[mcp_server],
    model=OpenAIResponsesModel(model=MODEL_NAME, openai_client=client),
    tools=[],
    output_type=LabelOutput,
)


async def main() -> None:
    await mcp_server.connect()

    message = (
        "Get issue #2759 from Azure-Samples/azure-search-openai-demo. Decide on the most appropriate label for it."
    )

    result = await Runner.run(starting_agent=agent, input=message)

    # Print the structured response
    print(result.final_output)
    await mcp_server.cleanup()


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    asyncio.run(main())
