import os

import openai
from dotenv import load_dotenv

load_dotenv(override=True)

client = openai.OpenAI(
    base_url=os.environ["NIM_ENDPOINT"],
    api_key="none")

response = client.responses.create(
    model=os.environ["NIM_MODEL"],
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)