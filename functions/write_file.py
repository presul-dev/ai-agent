import os

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
