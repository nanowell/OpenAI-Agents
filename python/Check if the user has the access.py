import os
import sys
import stat


def main():
    if len(sys.argv) != 2:
        print("Usage: {} <file or directory>".format(sys.argv[0]))
        sys.exit(1)

    path = sys.argv[1]
    print("Checking {}".format(path))
    try:
        mode = os.stat(path).st_mode
    except FileNotFoundError:
        print("File or directory not found")
        sys.exit(1)

    if stat.S_ISDIR(mode):
        print("{} is a directory".format(path))
    elif stat.S_ISREG(mode):
        print("{} is a regular file".format(path))
    else:
        print("{} is a special file".format(path))

    for access in [os.R_OK, os.W_OK, os.X_OK]:
        if os.access(path, access):
            print("{} is {}able".format(path, {os.R_OK: "read", os.W_OK: "write", os.X_OK: "execut"}[access]))
        else:
            print("{} is not {}able".format(path, {os.R_OK: "read", os.W_OK: "write", os.X_OK: "execut"}[access]))
