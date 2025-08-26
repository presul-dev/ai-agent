import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    test_dir = os.path.join(working_directory, directory)
    abs_test_dir = os.path.abspath(test_dir)
    items = []
    try:
        if abs_test_dir.startswith(os.path.abspath(working_directory)):
            if os.path.isdir(abs_test_dir):
                contents = os.listdir(abs_test_dir)
                for item in contents:
                    abs_item = os.path.join(abs_test_dir, item)
                    size = os.path.getsize(abs_item)
                    is_dir = os.path.isdir(abs_item)
                    items.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
                return "\n".join(items)
            else:
                return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

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