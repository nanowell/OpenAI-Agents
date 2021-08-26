import os
import sys
import subprocess
from pathlib import Path


def main():
    """Main function"""

    # Get the steamvr installation directory.
    steamvr_dir = get_steamvr_dir()

    # Check if SteamVR is installed.
    if not steamvr_dir:
        print("SteamVR is not installed.")
        return 1

    if check_steamvr():
        print("SteamVR is running.")

        while True:
            answer = input("Do you want to close it? [y/n] ")

            if answer == "y": break;

            elif answer == "n": return 0;

            else: continue;

        subprocess.call(["taskkill", "/IM", "SteamVR.exe"])

    for file in os.listdir(steamvr_dir):
        if file.startswith("openxr_loader_") and file.endswith(".dll"):
            os.remove(os.path.join(steamvr_dir, file))

    return 0


def get_steamvr_dir():
    """Get the SteamVR installation directory."""

    steamvr_dir = Path(os.environ["ProgramFiles(x86)"]) / "Steam" / "steamapps" / "common" / "SteamVR"

    if not steamvr_dir.is_dir():
        return None

    return str(steamvr_dir)


def check_steamvr():
    """Check if SteamVR is running."""

    for process in os.popen("tasklist").read().splitlines()[4:]:
        if process.split()[0] == "SteamVR.exe":
            return True

    return False


if __name__ == '__main__':
    sys.exit(main())