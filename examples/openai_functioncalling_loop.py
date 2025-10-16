import os
import json
import logging

import openai
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)
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
    {
        "type": "function",
        "name": "lookup_movies",
        "description": "Lookup movies playing in a given city name or zip code.",
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {
                    "type": "string",
                    "description": "The city name",
                },
                "zip_code": {
                    "type": "string",
                    "description": "The zip code",
                },
            },
            "additionalProperties": False,
        },
    },
]


# ---------------------------------------------------------------------------
# Tool (function) implementations
# ---------------------------------------------------------------------------
def lookup_weather(city_name: str | None = None, zip_code: str | None = None) -> str:
    """Looks up the weather for given city_name and zip_code."""
    location = city_name or zip_code or "unknown"
    # In a real implementation, call an external weather API here.
    return {
        "location": location,
        "condition": "rain showers",
        "rain_mm_last_24h": 7,
        "recommendation": "Good day for indoor activities if you dislike drizzle.",
    }


def lookup_movies(city_name: str | None = None, zip_code: str | None = None) -> str:
    """Returns a list of movies playing in the given location."""
    location = city_name or zip_code or "unknown"
    # A real implementation could query a cinema listings API.
    return {
        "location": location,
        "movies": [
            {"title": "The Quantum Reef", "rating": "PG-13"},
            {"title": "Storm Over Harbour Bay", "rating": "PG"},
            {"title": "Midnight Koala", "rating": "R"},
        ],
    }


tool_mapping = {
    "lookup_weather": lookup_weather,
    "lookup_movies": lookup_movies,
}


# ---------------------------------------------------------------------------
# Conversation loop
# ---------------------------------------------------------------------------
messages = [
    {"role": "system", "content": "You are a tourism chatbot."},
    {"role": "user", "content": "Is it rainy enough in Sydney to watch movies and which ones are on?"},
]

while True:
    response = client.responses.create(
        model=model_name,
        input=messages,  # includes prior tool outputs
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False,  # ensure sequential tool calls
    )
    for item in response.output:
        if item.type == "reasoning":
            print("REASONING STEP")
        if (item and hasattr(item, "type") and item.type == "function_call"):
            tool_call = item
            print(f"\nFUNCTION CALL DETECTED: {tool_call.name}")
            print(f"FUNCTION ARGUMENTS: {tool_call.arguments}")
            
            try:
                # Standardize argument parsing assuming JSON format
                args = json.loads(tool_call.arguments) if tool_call.arguments else {}
                print(f"PARSED ARGUMENTS: {args}")
                
                # Append the function call to the conversation
                messages.append({
                    "type": "function_call",
                    "call_id": tool_call.call_id,
                    "name": tool_call.name,
                    "arguments": tool_call.arguments
                })
                
                # Map the function call to the actual function
                function_map = {
                    "lookup_weather": lookup_weather,
                    "lookup_movies": lookup_movies,
                }
                
                # Execute the function
                if tool_call.name in function_map:
                    print(f"\nEXECUTING FUNCTION: {tool_call.name}")
                    
                    # Call the function with the parsed arguments
                    function_result = function_map[tool_call.name](**args)
                    print(f"FUNCTION RESULT: {function_result}")
                else:
                    function_result = f"Error: Function {tool_call.name} not found"
                    print(f"ERROR: {function_result}")
                
                # Add the function result to the conversation
                messages.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(function_result)
                })
                
                # Continue to the next iteration to process any more function calls
                continue
            except Exception as e:
                error_msg = f"Error during function execution: {e}"
        else:
            # No more function calls, capture the final assistant response
            if hasattr(response, 'output_text') and response.output_text:
                assistant_response = response.output_text
                messages.append({"role": "assistant", "content": assistant_response})
                print(f"\nFINAL RESPONSE: '{assistant_response}'")
                break