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
    with open(python_files[0], 'r') as file:
        contents = file.read()
    
    return contents


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
