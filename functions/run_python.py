import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(joined_path)
    abs_working_directory = os.path.abspath(working_directory)
    try:
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            if not os.path.exists(abs_file_path):
                return f'Error: File "{file_path}" not found.'
            if not file_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file.'
            result = subprocess.run(["python", abs_file_path] + args, capture_output=True, timeout=30,
                                    cwd=abs_working_directory, text=True)
            output = []
            if result.stdout:
                output.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output.append(f"STDERR: {result.stderr}")
            if result.returncode != 0:
                output.append(f"Process exited with code {result.returncode}")
            if not output:
                return "No output produced."
            return "\n".join(output)
    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files.  Limited to the working directory. Accepts multiple arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory, relative to the working directory, to run python files from. "
                            "If not provided, runs python files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to pass to execution of the python file. If no argument is provided "
                            "runs the python file without arguments.",
            ),
        },
    ),
)