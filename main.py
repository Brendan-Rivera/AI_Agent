import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import functions.call_function as cf

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

model = "gemini-2.0-flash-001"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request. You can perform the following operations:

- List files and directories
- Examine file content
- Run python files
- Write to Python files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the contents of the file in the specified directory along with a limit of 10,000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to print file content from, relative to the working directory. If not provided, it returns an error.",
            ),
        },
    ),
)

schema_get_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the file in the specified directory along with the content being a provided parameter, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write content to, relative to the working directory. If not provided, it returns an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file, relative to the working directory. If none is provided, nothing will be written"
            )
        },
    ),
)

schema_get_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Allows the user to run a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory. If not provided, it returns an error.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_get_write_file,
        schema_get_run_python
    ]
)

if len(sys.argv) < 2:
    print("No arguments provided. Usage: script.py '<your prompt here>'")
    sys.exit(1)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(model=model, contents=messages,
                                          config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
                                          )

if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print(f"\nUser prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if not response.function_calls:
         print(response.text)

MAX_STEPS = 20
for step in range(MAX_STEPS):
    function_was_called = False
    for candidate in response.candidates:
        if candidate.content:
            messages.append(candidate.content)
    if response.function_calls is None:
        function_was_called = True

    if not function_was_called:
        if response.text:
            print(response.text)
        else:
            print("No response from model.")
        break

    for function_call_part in response.function_calls:
                function_was_called = True
                try:
                    function_call_result = cf.call_function(function_call_part)
                    fc_result = function_call_result.parts[0].function_response.response["result"]
                    messages.append(types.Content(role="model", parts=[types.Part(text=fc_result)]))
                    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                         print(f"-> {fc_result}")
                except Exception as e:
                    raise Exception(f"No result returned from function call result. Exception {e}")

    
    
    response = client.models.generate_content(model=model,
                                               contents=messages,
                                               config=types.GenerateContentConfig(
                                               tools=[available_functions],
                                               system_instruction=system_prompt
                                                ),
                                            )
else:
    print("Reached maximum number of iterations without completion.")