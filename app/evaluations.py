import sys

def evaluate(command):
    if "exit" in command:
        sys.exit(0)
    elif "echo" in command:
        return command[5:]
    return f"{command}: command not found"