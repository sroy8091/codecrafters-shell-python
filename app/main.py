import readline
import sys

from app.evaluations import evaluate
from app.mapping import command_evaluations


def completer(text: str, state: int) -> str | None:
    matches = [cmd + " " for cmd in command_evaluations if cmd.startswith(text)]
    return matches[state] if state < len(matches) else None

def main():
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        evaluate(command)


if __name__ == "__main__":
    main()
