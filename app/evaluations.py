import sys

from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = command.split()
    # print(premise in command_evaluations)
    if premise in command_evaluations:
        return command_evaluations[premise](*args)
    elif premise == "type":
        print(handle_type(premise, *args))
        return None
    else:
        print(f"{premise}: command not found")
        return None


def handle_type(premise, *args):
    if args[0] in command_evaluations:
        return f"{args[0]} is a shell builtin"
    else:
        return f"{premise}: command not found"
