import os

import openai
from dotenv import load_dotenv

load_dotenv(override=True)

client = openai.OpenAI(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none")

response = client.responses.create(
    model=os.environ["NIM_MODEL"],
    input="If a city starts offering free bike rentals during rush hour, how might different rental durations and locations impact the way people commute?",
    reasoning={
        "effort": "low",
    }
)


for item in response.output:
    if item.type == "message":
        print(f"🤖 Response: {item.content[0].text}")
    elif item.type == "reasoning":
        for content in item.content:
            print(f"💭 Reasoning: {content.text}")