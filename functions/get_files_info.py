#!/usr/bin/env python

import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))

        valid_target_dir = os.path.commonpath([target_dir, abs_path]) == abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        file_list: list[str] = []
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)
            f_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_list.append(f'- {file}: file_size={f_size}, is_dir={is_dir}')

        return '\n'.join(file_list) 
    except:
        return 'Error: Runtime error occured for get_files_info'
