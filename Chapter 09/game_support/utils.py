import os
import glob

def get_code(folder_path):
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        return None

    # Get a list of all Python files in the folder
    python_files = glob.glob(os.path.join(folder_path, "*.py"))

    # Sort the files alphabetically
    python_files.sort()

    # Check if there are any Python files in the folder
    if not python_files:
        return None

    # Read and return the contents of the first Python file
    contents = get_raw_code(python_files[0])
    
    return contents


def get_raw_code(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Remove inline comments
    lines = [line.split('#')[0] for line in lines]

    # Remove blank lines and lines that became blank after removing inline comments
    lines = [line for line in lines if line.strip()]

    return ''.join(lines)



def load_requirements(file_path):
    try:
        with open(file_path, 'r') as file:
            requirements = [line.strip() for line in file.readlines()]
        return requirements
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
