import sys

from app.evaluations import evaluate


def main():
    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")

        # Wait for user input
        command = input()
        print(evaluate(command))


if __name__ == "__main__":
    main()
