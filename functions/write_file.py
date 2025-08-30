import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_file = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(working_file)
    abs_working_directory = os.path.abspath(working_directory)
    try:
        if abs_file_path.startswith(abs_working_directory):
            if not os.path.exists(abs_file_path):
                os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            with open(working_file, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Writes file to the file_path within the working directory."
                            "Writes to working directory if no file path is provided",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
    ),
)