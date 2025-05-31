import io
import os
import shlex
import shutil
import subprocess
from contextlib import redirect_stdout

from app.helper import write_builtin_output
from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = shlex.split(command)

    output_location = None
    error_location = None
    append_mode = False

    if ">" in args or "1>" in args:
        output_location = args[-1]
        args = args[:-2]

    if "2>" in args:
        error_location = args[-1]
        args = args[:-2]

    if ">>" in args or "1>>" in args:
        output_location = args[-1]
        args = args[:-2]
        append_mode = True

    if premise in command_evaluations:
        return evaluate_builtin_commands(premise, args, output_location, error_location, append_mode)
    elif shutil.which(premise):
        return evaluate_external_commands(premise, args, output_location, error_location, append_mode)
    else:
        print(f"{premise}: command not found")
        return None


def evaluate_builtin_commands(premise, args, output_location, error_location, append_mode):
    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            command_evaluations[premise](*args)

        output = output_buffer.getvalue()

        # If save_location is specified, write to file
        if output_location:
            write_builtin_output(output_location, output, append_mode)
            return None
        else:
            if error_location:
                write_builtin_output(error_location, "")
            print(output, end='')
            return None
    except Exception as e:
        if error_location:
            write_builtin_output(error_location, f"{premise}: {e.args[0]}")
        else:
            print(e.args[0], end='')
        return None

def evaluate_external_commands(premise, args, output_location, error_location, append_mode):
    if output_location:
        if append_mode:
            # with open(output_location, 'a') as f:
            #     if os.path.getsize(output_location) > 0:  # Check if file is not empty
            #         f.write('\n')
            with open(output_location, 'a') as f:
                return subprocess.run([premise] + args, stdout=f)
        else:
            with open(output_location, 'w') as f:
                return subprocess.run([premise] + args, stdout=f)
    elif error_location:
        with open(error_location, 'w') as f:
            return subprocess.run([premise] + args, stderr=f)
    else:
        return subprocess.run([premise] + args, capture_output=False)