import os
import subprocess

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
