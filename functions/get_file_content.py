import os

def get_file_content(working_directory, file_path):
    working_dir = os.path.abspath(working_directory)
    f_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not os.path.commonpath([f_path, working_dir]) == working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(f_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    

    try:
        MAX_CHARS = 10000
        with open(f_path, "r") as file:
            file_content = file.read(MAX_CHARS)
            file_content += f'\n[...File "{file_path}" truncated at 10000 characters]'
            return file_content
    except Exception as e:
        print(f"Error: An error has occured when attempting to open a file.\n{e}")