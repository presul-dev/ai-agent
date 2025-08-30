import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    working_file = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(working_file)
    abs_working_dir = os.path.abspath(working_directory)
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        if abs_file_path.startswith(abs_working_dir):
            with open(abs_file_path, "r") as f:
                file_contents = f.read(MAX_CHARS + 1)
                if len(file_contents) > MAX_CHARS:
                    return file_contents[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                else:
                    return file_contents
        else:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows the contents of the file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path is relative to the working directory.  If no path is provided, "
                            "it uses the working directory",
            ),
        },
    ),
)