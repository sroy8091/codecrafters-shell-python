import readline
import sys

from app.auto_complete_matcher import complete, display_matches_hook
from app.evaluations import evaluate


def main():
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    readline.set_completion_display_matches_hook(display_matches_hook)

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        evaluate(command)


if __name__ == "__main__":
    main()
