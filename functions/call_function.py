from functions import get_files_info as gfi
from functions import get_file_content as gfc
from functions import write_file as wf
from functions import run_python_file as rp
from google.genai import types

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args or {}

    # Log function call
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # Add the working_directory to args explicitly
    args["working_directory"] = "calculator"

    # Function name -> callable map
    dispatch_table = {
        "get_files_info": gfi.get_files_info,
        "get_file_content": gfc.get_file_content,
        "write_file": wf.write_file,
        "run_python_file": rp.run_python_file
    }

    # Handle unknown function
    if function_name not in dispatch_table:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )

    try:
        # Call the function with keyword arguments
        function_result = dispatch_table[function_name](**args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Function raised an exception: {str(e)}"},
                )
            ]
        )

    # Log output if verbose
    if verbose:
        print(f"-> {function_result}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )