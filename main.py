#!/usr/bin/env python3

# Main file for my first agent based project

import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import system_prompt

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


def print_debug(response_data: GenerateContentResponse):
    print(f"Prompt tokens: {response_data.prompt_token_count}")
    print(f"Response tokens: {response_data.candidates_token_count}")


"""
Contains the functionality for our agent LOOP
"""


def generate_content(
    client: genai.Client, model: str, messages: list[types.Content], verbose: bool
) -> bool:
    response = get_chat_response(client, model, messages)

    # append candidate content to track AI responses
    for candidate in response.candidates or ():
        messages.append(candidate.content)

    # Check response validity and contents
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    if verbose:
        print_debug(response.usage_metadata)
    if not response.function_calls:
        print(f"Response:")
        print(response.text)
        return True

    # Execute function calls from the agent
    function_results = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)

        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")

        if verbose:
            print(f"-> {result.parts[0].function_response.response}")

        function_results.append(result.parts[0])

    # Allow the chatbot to see its function calls after iteration
    messages.append(types.Content(role="user", parts=function_results))

    return False


def main():
    # Parse command line arguments
    args = parse_arguments()

    # Initiate our genai Client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # Print response at token usage stats
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    complete: bool
    for _ in range(20):
        complete = generate_content(client, "gemini-2.5-flash", messages, args.verbose)

        if complete:
            break

    if not complete:
        print("Model reached maximum loops") 
        sys.exit(1)


if __name__ == "__main__":
    main()
