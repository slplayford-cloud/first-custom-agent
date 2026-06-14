#!/usr/bin/env python

from functions.get_file_content import get_file_content

def main():
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    result = get_file_content("calculator", "main.py")
    print(f"main.py length: {len(result)}")
    print(f"main.py - \n{result}")

    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"calculator.py length: {len(result)}")
    print(f"calculator.py - \n{result}")

    result = get_file_content("calculator", "/bin/cat")
    print(f"/bin/cat - \n{result}")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"pkg/does_not_exist.py - \n{result}")

if __name__ == "__main__":
    main()
