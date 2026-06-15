#!/usr/bin/env python

import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # Check if the file_path falls within the working directory
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the file is a regular file
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Make any subdirectories needed to get to the filepath
        os.makedirs(name=file_path, exist_ok=True)


        # Write to the file
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except:
        return f'Error: RuntimeError occured while running write_file()'
