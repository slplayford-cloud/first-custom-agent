#!/usr/bin/env python

import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_file = os.path.commonpath([target_file, abs_path]) == abs_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"' 

        with open(target_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content 
    except:
        return 'Error: Runtime error occured for get_file_content()'

