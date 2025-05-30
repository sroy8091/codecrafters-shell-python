import shutil
import subprocess

from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = command.split()
    # print(premise in command_evaluations)
    if premise in command_evaluations:
        return command_evaluations[premise](*args)
    elif shutil.which(premise):
        return subprocess.run([premise] + args, capture_output=False)
    else:
        print(f"{premise}: command not found")
        return None
