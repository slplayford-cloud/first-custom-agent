#!/usr/bin/env python3

# Main file for my first agent based project

import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    print("Gemini api key not found")
    raise RuntimeError

"""
Parse command line arguments for our ai agent main.py file
"""


def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    return args


"""
function which allows us to chat with our given AI provider
"""


def get_chat_response(client: genai.Client, model: str, messages: list[types.Content]):
    return client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )


"""
Prints a simple debug message for when --verbose is used
"""


def print_debug(user_prompt: str, response_data: GenerateContentResponse):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response_data.prompt_token_count}")
    print(f"Response tokens: {response_data.candidates_token_count}")


def main():
    # Parse command line arguments, initiate a genai Client and conversation messages
    args = parse_arguments()
    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    response = get_chat_response(client, "gemini-2.5-flash", messages)

    # Print response at token usage stats
    if args.verbose:
        print_debug(args.user_prompt, response.usage_metadata)

    # Execute function calls from the agent
    function_results = []
    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)

            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")

            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")

            function_results.append(result.parts[0])
    else:
        print(f"Response:")
        print(response.text)


if __name__ == "__main__":
    main()
