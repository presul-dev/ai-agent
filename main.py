import os
from sys import argv
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
ai_model = "gemini-2.0-flash-001"
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

if len(argv) <= 1:
    print("No arguments provided")
    exit(1)

user_prompt = argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(model='gemini-2.0-flash-001',
                                          contents=messages,
                                          config = types.GenerateContentConfig(
                                              system_instruction=system_prompt,
                                            ),
                                          )
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

print(response.text)
if "--verbose" in argv:
    print(f"User prompt: {argv[1]}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
