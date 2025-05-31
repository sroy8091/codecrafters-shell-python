import os
import readline
import shutil
import sys


def check_command_in_path(cmd):
    # Use shutil.which to find executable in PATH
    cmd_path = shutil.which(cmd)
    if cmd_path:
        return f"{cmd} is {cmd_path}"
    return None

def execute_type_cmd(cmd):
    if cmd in command_evaluations:
        print(f"{cmd} is a shell builtin")
    elif check_command_in_path(cmd):
        print(check_command_in_path(cmd))
    else:
        raise NotImplementedError(f"{cmd}: not found\n")

def execute_cd_cmd(args):
    if os.path.isdir(os.path.expanduser(args)):
        os.chdir(os.path.expanduser(args))
    else:
        raise FileNotFoundError(f"cd: {args}: No such file or directory\n")

def execute_history():
    history_length = readline.get_current_history_length()
    for i in range(1, history_length + 1):
        print(f" {i}  {readline.get_history_item(i)}")


command_evaluations = {
    "exit": lambda exit_code: sys.exit(int(exit_code)),
    "echo": lambda *args: print(" ".join(args)),
    "type": execute_type_cmd,
    "pwd": lambda : print(os.getcwd()),
    "cd": execute_cd_cmd,
    "history": execute_history
}