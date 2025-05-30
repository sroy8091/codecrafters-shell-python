import os
import shutil


def check_command_in_path(cmd):
    # Use shutil.which to find executable in PATH
    cmd_path = shutil.which(cmd)
    if cmd_path:
        return f"{cmd} is {cmd_path}"
    return None

def print_file_content(args):
    content = []
    for file in args:
        with open(file, 'r') as f:
            content.append(f.read())

    print(*content)


command_evaluations = {
    "exit": lambda exit_code: os._exit(int(exit_code)),
    "echo": lambda *args: print(" ".join(args)),
    "type": lambda cmd: print(f"{cmd} is a shell builtin")
    if cmd in command_evaluations
    else (print(check_command_in_path(cmd)) if check_command_in_path(cmd)
          else print(f"{cmd}: not found")),
    "pwd": lambda : print(os.getcwd()),
    "cd": lambda args: os.chdir(os.path.expanduser(args))
    if os.path.isdir(os.path.expanduser(args))
    else print(f"cd: {args}: No such file or directory"),
    # "cat": lambda *args: print_file_content(args)
}