from __future__ import print_function
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Package dependencies:
#
# build-essential
# libncurses5-dev
# libssl-dev

# -----------------------------------------------------------------------------

def main():
    """
    Main program.

    """

    build_dir = tempfile.mkdtemp()
    os.chdir(build_dir)

    print("Downloading kernel source...")
    if not download_source():
        print("Error downloading kernel source.  Exiting...")
        sys.exit(1)

    print("Building kernel...")
    if not build_kernel():
        print("Error building kernel.  Exiting...")
        sys.exit(1)

    print("Installing kernel...")
    if not install_kernel():
        print("Error installing kernel.  Exiting...")
        sys.exit(1)

    print("Cleaning up...")
    if not cleanup():
        print("Error cleaning up.  Exiting...")
        sys.exit(1)

    print("Finished.")
    sys.exit(0)

# -----------------------------------------------------------------------------

def build_kernel():
    """
    Build the kernel.

    """

    # Configure the build.
    if not run_command("./build_rpi_kernel.sh"):
        return False

    # Build the kernel.
    if not run_command("make -j4"):
        return False

    return True

# -----------------------------------------------------------------------------

def build_modules():
    """
    Build kernel modules.

    """

    # Build the kernel modules.
    if not run_command("make -C /lib/modules/$(uname -r)/build M=$(pwd) modules"):
        return False

    return True

# -----------------------------------------------------------------------------

def cleanup():
    """
    Clean up the build directory.

    """



    return True

# -----------------------------------------------------------------------------

def download_source():
    """
    Download the kernel source.

    """

    # Download the source.
    if not run_command("wget https://github.com/raspberrypi/linux/archive/rpi-3.18.y.zip"):
        return False

    # Unzip the source.
    if not run_command("unzip rpi-3.18.y.zip"):
        return False

    return True

# -----------------------------------------------------------------------------

def install_kernel():
    """
    Install the kernel.

    """

    # Install the kernel.
    if not run_command("sudo make modules_install"):
        return False

    # Install the kernel headers.
    if not run_command("sudo make headers_install"):
        return False

    return True

# -----------------------------------------------------------------------------

def run_command(command):
    """
    Run a command.

    """

    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as err:
        print("Command failed: " + str(err))
        return False

    return True

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()