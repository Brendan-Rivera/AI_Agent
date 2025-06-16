import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory

    dir_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)

    if not os.path.commonpath([dir_path, working_path]) == working_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'

    try:
        list_dir = os.listdir(dir_path)
    except Exception as e:
        return f'Error reading directory contents: {e}'

    lines = []
    for item in list_dir:
        item_path = os.path.join(dir_path, item)
        try:
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"{item}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            lines.append(f"{item}: Error reading file info: {e}")

    return "\n".join(lines)


    
