# Check if the user has the access to the file or directory


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

    if os.access(path, os.R_OK):
        print("{} is readable".format(path))
    else:
        print("{} is not readable".format(path))

    if os.access(path, os.W_OK):
        print("{} is writable".format(path))
    else:
        print("{} is not writable".format(path))

    if os.access(path, os.X_OK):
        print("{} is executable".format(path))
    else:
        print("{} is not executable".format(path))


if __name__ == "__main__":
    main()

