import shlex
import shutil
import subprocess

from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = shlex.split(command)
    # sanitized_args = sanitise_commands(args)

    if premise in command_evaluations:
        return command_evaluations[premise](*args)
    elif shutil.which(premise):
        return subprocess.run([premise] + args, capture_output=False)
    else:
        print(f"{premise}: command not found")
        return None


def sanitise_commands(args):
    result = []
    for item in args:
        result.append(item.strip('"').strip("'"))
    return result