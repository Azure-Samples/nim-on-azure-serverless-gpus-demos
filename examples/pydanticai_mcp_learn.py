"""PydanticAI + Microsoft Learn MCP example.

This example uses the public Microsoft Learn MCP HTTP server instead of a local MCP server.

Environment prerequisites:
    - Set `NIM_ENDPOINT` and `NIM_MODEL` in your environment (e.g. via a `.env` file) so the NIM-backed
        OpenAI Responses client can route requests.
    - (Optional) Set `APPLICATIONINSIGHTS_CONNECTION_STRING` if you have observability wired elsewhere.
"""

import asyncio
import logging
import os
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import CallToolFunc, MCPServerStreamableHTTP, ToolResult
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider

# Setup the OpenAI client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

client = AsyncOpenAI(base_url=os.environ["NIM_ENDPOINT"], api_key="none")

model = OpenAIResponsesModel(
    os.environ["NIM_MODEL"],
    provider=OpenAIProvider(openai_client=client),
    profile=OpenAIModelProfile(
        openai_responses_requires_function_call_status_none=True, supports_json_schema_output=True
    ),
)


async def process_tool_call(
    ctx: RunContext[int],
    call_tool: CallToolFunc,
    name: str,
    tool_args: dict[str, Any],
) -> ToolResult:
    """A tool call processor that passes along the deps."""
    logging.info(f"Processing tool call to {name} with args {tool_args} and deps {ctx.deps}")
    return await call_tool(name, tool_args, {"deps": ctx.deps})


server = MCPServerStreamableHTTP(url="https://learn.microsoft.com/api/mcp", process_tool_call=process_tool_call)


class Answer(BaseModel):
    """Answer with citations."""

    answer: str = Field(description="The answer to the user's question.")
    citations: list[str] = Field(description="List of URLs used as citations for the answer.")


agent: Agent[None, str] = Agent(
    model,
    system_prompt="Use the tools to answer the question and provide citations.",
    toolsets=[server],
    # output_type=NativeOutput(Answer)
)


async def main():
    result = await agent.run("Does Azure offer serverless GPUs?")
    print(result.output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(main())
