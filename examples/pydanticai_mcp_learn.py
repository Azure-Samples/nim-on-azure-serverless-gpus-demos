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
from pydantic_ai import Agent, NativeOutput, RunContext
from pydantic_ai.mcp import CallToolFunc, MCPServerStreamableHTTP, ToolResult
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider
from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown

# Setup the OpenAI client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
    logger.info(f"Processing tool call to {name} with args {tool_args}")
    return await call_tool(name, tool_args, {"deps": ctx.deps})


server = MCPServerStreamableHTTP(url="https://learn.microsoft.com/api/mcp", process_tool_call=process_tool_call)


class Citation(BaseModel):
    """Citation model."""
    url: str = Field(description="The URL of the citation.")
    title: str = Field(description="The title of the citation.")

class Answer(BaseModel):
    """Answer with citations."""
    answer: str = Field(description="The answer to the user's question.")
    citations: list[Citation] = Field(description="List of citations for the answer.")


agent = Agent(
    model,
    system_prompt="Use tools to answer question. Your answer should be in markdown (lists, headings, tables, quotes, etc) and include citations.",
    toolsets=[server],
    output_type=NativeOutput(Answer)
)

async def main():
    result = await agent.run("Does Azure offer serverless GPUs?")
    
    console = Console()
    console.print(Markdown(result.output.answer))
    citations_md = "\n\n## Citations\n\n" + "\n".join(
        f"- [{citation.title}]({citation.url})" for citation in result.output.citations
    )
    console.print(Markdown(citations_md))


if __name__ == "__main__":
    asyncio.run(main())
