import os
import subprocess

def run_python_file(working_directory, file_path):
    w_dir = os.path.abspath(working_directory)
    f_path = os.path.abspath(os.path.join(working_directory,file_path))
    to_return = os.path.basename(f_path)
    if not os.path.commonpath([f_path, w_dir]) == w_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(f_path):
        return f'Error: File "{to_return}" not found.'
    
    if not f_path.endswith(".py"):
        
        return f'Error: "{to_return}" is not a Python file.'

    try:
        run_file = subprocess.run(["python3", f_path], timeout=30, cwd=w_dir, capture_output=True, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = f"Process exited with code {run_file.returncode}"
    if run_file.stdout.strip():
        output += f"\n\nSTDOUT:\n{run_file.stdout}"
    if run_file.stderr.strip():
        output += f"\n\nSTDERR:\n{run_file.stderr}"
    if not run_file.stdout.strip() and not run_file.stderr.strip():
        output += "\n\nNo output produced."
    return output