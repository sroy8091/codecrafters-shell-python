import io
import shlex
import shutil
import subprocess
from contextlib import redirect_stdout

from app.mapping import command_evaluations


def evaluate(command):
    premise, *args = shlex.split(command)
    save_location = None
    if ">" in args or "1>" in args:
        save_location = args[-1]
        args = args[:-2]

    if premise in command_evaluations:
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            command_evaluations[premise](*args)

        output = output_buffer.getvalue()

        # If save_location is specified, write to file
        if save_location:
            with open(save_location, 'w') as f:
                f.write(output)
            return None
        else:
            print(output, end='')

        # return command_evaluations[premise](*args)
    elif shutil.which(premise):
        if save_location:
            with open(save_location, 'w') as f:
                return subprocess.run([premise] + args, stdout=f)
        else:
            return subprocess.run([premise] + args, capture_output=False)
    else:
        print(f"{premise}: command not found")
        return None