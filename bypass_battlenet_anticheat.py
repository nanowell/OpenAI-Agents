"""
Bypasses battle.net anti-cheat in Windows 10.
This script will bypass battle.net anti-cheat
"""

import os
import sys
import time
import subprocess
import winreg

def main():
    """
    Main function
    """
    # Check if Windows 10
    if sys.getwindowsversion().major != 10:
        print("This script is only for Windows 10!")
        sys.exit(1)

    # Check if 64-bit Windows
    if sys.getwindowsversion().architecture()[0] != 64:
        print("This script is only for 64-bit Windows!")
        sys.exit(1)

    # Check if Battle.net is running
    if not is_battle_net_running():
        print("Battle.net is not running!")
        sys.exit(1)

    # Check if Battle.net is running as admin
    if not is_battle_net_admin():
        print("Battle.net is not running as admin!")
        sys.exit(1)

    # Check if Battle.net is running as admin
    if is_battle_net_bypassed():
        print("Battle.net is already bypassed!")
        sys.exit(1)

    # Bypass Battle.net
    print("Bypassing Battle.net...")
    bypass_battle_net()

    # Check if Battle.net is running as admin
    if is_battle_net_bypassed():
        print("Battle.net is now bypassed!")
    else:
        print("Battle.net is still not bypassed!")
        sys.exit(1)

def is_battle_net_running():
    """
    Checks if Battle.net is running
    """
    try:
        subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq Battle.net.exe"])
        return True
    except subprocess.CalledProcessError:
        return False

def is_battle_net_admin():
    """
    Checks if Battle.net is running as admin
    """
    try:
        subprocess.check_output(["sc", "query", "type=", "service", "state=", "all", "bufsize=", "4096", "user=", "NT AUTHORITY\SYSTEM"])
        return True
    except subprocess.CalledProcessError:
        return False

def is_battle_net_bypassed():
    """
    Checks if Battle.net is already bypassed
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Blizzard Entertainment\\Battle.net")
        winreg.QueryValueEx(key, "AllowInsecure")
        return True
    except OSError:
        return False

def bypass_battle_net():
    """
    Bypasses Battle.net
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Blizzard Entertainment\\Battle.net", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "AllowInsecure", 0, winreg.REG_DWORD, 1)

if __name__ == "__main__":
    main()
