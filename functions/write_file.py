import os

def write_file(working_directory, file_path, content):
    working_dir = os.path.abspath(working_directory)
    f_path = os.path.abspath(os.path.join(working_directory,file_path))

    # Ensure the target file is within the working directory
    if not os.path.commonpath([f_path, working_dir]) == working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Ensure the directory exists
    dir_name = os.path.dirname(f_path)
    os.makedirs(dir_name, exist_ok=True)

    # Try writing to the file
    try:
        with open(f_path, "w") as file:
            file.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
