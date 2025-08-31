import os
from sys import argv

import typing_extensions
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from config import MAX_ITERATIONS

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in function_map:
        func = function_map[function_call_part.name]
        args = function_call_part.args
        args["working_directory"] = "./calculator"
        function_result = func(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ]
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ]
        )




load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
ai_model = "gemini-2.0-flash-001"

if len(argv) <= 1:
    print("No arguments provided")
    exit(1)

user_prompt = argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
def generate_content():
    response = client.models.generate_content(model='gemini-2.0-flash-001',
                                              contents=messages,
                                              config = types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt,
                                                ),
                                              )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    for candidate in response.candidates:
        messages.append(candidate.content)
    verbose = "--verbose" in argv

    if response.function_calls:
        function_call_result = call_function(response.function_calls[0], verbose)
        function_call_response = function_call_result.parts[0].function_response.response
        if function_call_response:
            messages.append(types.Content(role="user", parts=[function_call_result.parts[0]]))
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            raise Exception(f"Fatal error trying to run")
        #print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
    else:
        return response.text

    if verbose:
        print(f"User prompt: {argv[1]}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

i=0
while i < MAX_ITERATIONS:
    i+= 1
    try:
        result = generate_content()
        if result:
            print(result)
            break
    except Exception as e:
        print(e)
else:
    print(f"Iteration cap reached: {MAX_ITERATIONS} iterations")
