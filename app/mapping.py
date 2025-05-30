import os

command_evaluations = {
    "exit": lambda exit_code: os._exit(int(exit_code)),
    "echo": lambda *args: print(" ".join(args)),
    "type": None,
}