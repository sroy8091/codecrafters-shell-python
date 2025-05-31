import os
import readline
import sys

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
    commands = set(list(command_evaluations.keys()) + list(get_executables_from_path()))
    matches = [cmd + " " for cmd in commands if cmd.startswith(text)]
    matches.sort()
    return matches[state] if state < len(matches) else None

def display_matches_hook(substitution, matches, longest_match_length):
    """Custom display function for matches"""
    print()  # Move to a new line

    print(*matches, sep=" ")
    print("$ ", end="")  # Print prompt on new line
    sys.stdout.write(readline.get_line_buffer())  # Write current input
    sys.stdout.flush()