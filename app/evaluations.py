import sys

from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = command.split()
    # print(premise in command_evaluations)
    if premise == "type":
        print(handle_type(premise, *args))
        return None
    elif premise in command_evaluations:
        return command_evaluations[premise](*args)
    else:
        print(f"{premise}: command not found")
        return None


def handle_type(premise, *args):
    if args[0] in command_evaluations:
        return f"{args[0]} is a shell builtin"
    else:
        return f"{args[0]}: not found"
