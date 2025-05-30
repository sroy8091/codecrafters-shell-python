import sys

from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = command.split()
    # print(premise in command_evaluations)
    if premise in command_evaluations:
        return command_evaluations[premise](*args)
    else:
        print(f"{premise}: command not found")
        return None
