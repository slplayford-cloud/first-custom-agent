#!/usr/bin/env python

import os
import subprocess

def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None
) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output: list[str] = []
        if process.returncode != 0:
            output.append("Process exited with code X")
        if not process.stdout and not process.stderr:
            output.append("No output produced")
        else:
            output.append(f"STDOUT: {process.stdout}")
            output.append(f"STDERR: {process.stderr}")

        return '\n'.join(output)

    except e:
        return f"Error: executing Python file: {e}"
