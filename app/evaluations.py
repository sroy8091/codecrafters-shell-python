import io
import os
import shlex
import shutil
import subprocess
import sys
from contextlib import redirect_stdout

from app.helper import write_builtin_output
from app.mapping import command_evaluations


def execute_pipe_command(command, input_pipe=None, output_pipe=None):
    # Fork a new process
    pid = os.fork()

    if pid == 0:  # Child process
        try:
            # Set up pipes for input/output if provided
            if input_pipe:
                os.dup2(input_pipe, sys.stdin.fileno())
                os.close(input_pipe)
            if output_pipe:
                os.dup2(output_pipe, sys.stdout.fileno())
                os.close(output_pipe)

            # Split command into premise and args
            premise, *args = shlex.split(command)

            # Handle builtin commands
            if premise in command_evaluations:
                # Redirect stdout to capture builtin output
                command_evaluations[premise](*args)
                sys.exit(0)
            elif shutil.which(premise):
                # Execute external command
                os.execvp(premise, [premise] + args)
            else:
                print(f"{premise}: command not found")
                sys.exit(1)
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)

    return pid


def evaluate(command):
    if "|" in command:
        # Split the command by pipes
        commands = [cmd.strip() for cmd in command.split("|")]

        # Create pipes for each command pair
        pipes = []
        for _ in range(len(commands) - 1):
            pipes.append(os.pipe())

        # Execute commands with pipes
        processes = []
        for i, cmd in enumerate(commands):
            input_pipe = pipes[i - 1][0] if i > 0 else None
            output_pipe = pipes[i][1] if i < len(commands) - 1 else None

            pid = execute_pipe_command(cmd, input_pipe, output_pipe)
            processes.append(pid)

        # Close all pipe ends in the parent process
        for read_fd, write_fd in pipes:
            os.close(read_fd)
            os.close(write_fd)

        # Wait for all child processes to complete
        for pid in processes:
            os.waitpid(pid, 0)

        return

    premise, *args = shlex.split(command)
    output_location, error_location, append_mode, args = check_for_redirections(args)

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
            write_builtin_output(error_location, f"{premise}: {e.args[0]}", append_mode)
        else:
            print(e.args[0], end='')
        return None

def evaluate_external_commands(premise, args, output_location, error_location, append_mode):
    if output_location:
        if append_mode:
            with open(output_location, 'a') as f:
                return subprocess.run([premise] + args, stdout=f)
        else:
            with open(output_location, 'w') as f:
                return subprocess.run([premise] + args, stdout=f)
    elif error_location:
        if append_mode:
            with open(error_location, 'a') as f:
                return subprocess.run([premise] + args, stderr=f)
        with open(error_location, 'w') as f:
            return subprocess.run([premise] + args, stderr=f)
    else:
        return subprocess.run([premise] + args, capture_output=False)

def check_for_redirections(args):
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

    if "2>>" in args:
        error_location = args[-1]
        args = args[:-2]
        append_mode = True

    return output_location, error_location, append_mode, args
