import os

from app.mapping import command_evaluations


def get_executables_from_path():
    executables = set()
    # Get PATH directories
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)

    # Search each directory in PATH
    for directory in path_dirs:
        if os.path.exists(directory):
            # List all files in the directory
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                # Check if the file is executable
                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                    executables.add(file)
    return executables


def complete(text, state):
    # Combine builtin commands with executables from PATH
    commands = list(command_evaluations.keys()) + list(get_executables_from_path())
    # Filter commands that match the text
    matches = [cmd + " " for cmd in commands if cmd.startswith(text)]
    # Sort matches for consistent ordering
    matches.sort()
    return matches[state] if state < len(matches) else None
