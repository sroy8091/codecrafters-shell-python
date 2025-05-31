import os


def write_builtin_output(location, content, append_mode=False):
    if append_mode:
        with open(location, 'a') as f:
            f.write(content)
    else:
        with open(location, 'w') as f:
            f.write(content)
