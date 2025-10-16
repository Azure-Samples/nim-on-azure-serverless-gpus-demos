import os
import json

import openai
from dotenv import load_dotenv

load_dotenv(override=True)

client = openai.OpenAI(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none")
model_name = os.environ["NIM_MODEL"]

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

response = client.responses.create(
    model=model_name,
    input=[
        {"role": "user", "content": "What is the weather like in Paris today?"},
    ],
    tools=tools,
)

for item in response.output:
    if item.type == "message":
        print(f"🤖 Response: {item.content[0].text}")
    elif item.type == "reasoning":
        for content in item.content:
            print(f"💭 Reasoning: {content.text}")
    elif item.type == "function_call":
        arguments = ", ".join(
            f"{k}='{v}'" for k, v in json.loads(item.arguments).items()
        )
        print(f"🔧 Tool Call: {item.name}({arguments})")