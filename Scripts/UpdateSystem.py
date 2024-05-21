import os
import sys
import time

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   1,
        "Minor"     :   1,
        "Revision"  :   3
    }

# Print the script version:
def PrintScriptVersion() -> str:
    strVer = "v."
    strVer += __ScriptVersionNumber__["Major"].__str__()
    strVer += "."
    strVer += __ScriptVersionNumber__["Minor"].__str__()
    strVer += "."
    strVer += __ScriptVersionNumber__["Revision"].__str__()
    return strVer

# Print the script header presentation:
def PrintScriptPresentation() -> None:
    j = 0
    line = ""
    terminalSize = os.get_terminal_size()

    # Write a line divisor using 3/4 of console width
    while j < terminalSize.columns * 0.75:
        line += '-'
        j = j + 1
        pass
    print("\nUpdate System Script for Linux OS - ",PrintScriptVersion())
    print(line)
    pass

# Call the system package manager to execute a task:
def UpdateSys(packMng, packMngArgs):
    cmd = packMng + " " + packMngArgs
    os.system(cmd)
    pass

# Call to Snap Store to update the packages:
def UpdateSnap():
    os.system("snap refresh")
    pass

# Set the package manager to call:
packMng = "dnf"

# --------------------------------- The script starts here ------------------------------- #

PrintScriptPresentation()
time.sleep(2)

if not sys.platform.startswith('linux'):
    print("This script is only for Linux OS")
    exit(1)

if os.getuid() != 0:
    print("[FAIL]::The script is not running with super user rights!")
    exit(2)

print("\nUpdating system packages...\n")
time.sleep(5.0)

UpdateSys(packMng, "upgrade")

UpdateSnap()

UpdateSys(packMng, "autoremove")
#UpdateSys(packMng, "clean --packages")

print("\nDone!\n")

exit(0)