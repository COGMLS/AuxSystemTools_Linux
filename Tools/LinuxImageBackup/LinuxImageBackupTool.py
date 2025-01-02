import os
import sys

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   0,
        "Minor"     :   1,
        "Revision"  :   0
    }

# Debug Script mode:
DEBUG_SCRIPT = False

# Control Variables:
bDebugScript = DEBUG_SCRIPT	        # Script Debug Mode
bVerboseMode = False                # Verbose Mode
bConfirmChanges = False             # Control if the changes must be confirmed
bCtrlShowHelp = False               # Show the script or run tasks
bRunAsAdmin = False                 # Control the admin. privileges

# Check for Debug parameter:
if not bDebugScript:
    for arg in sys.argv:
        if arg.lower() == "-debugscript":
            bDebugScript = True
            break
        pass
    pass

# -------------------------------- Script Internal Components -------------------------------- #

# Help command line:
helpCmd = ["-help","-h","-?"]

# Help info:
help = [
    "\nLinux Image Backup Tool",
    "PARAMETERS:",
    "\t<Param>\t<ParamInfo>",
]

# --------------------------------- Script Methods ---------------------------------- #

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
    print("\nLinux Image Backup - ",PrintScriptVersion())
    print(line)
    pass

# Test if there is no argument
def PrintHelp() -> None:
    if bCtrlShowHelp:
        i = 0
        for hlpStr in help:
            if i == 0:
                PrintScriptPresentation()
                pass
            else:
                print(hlpStr,"\n")
                pass
            i = i + 1
            pass
        exit(0)
        pass
    else:
        PrintScriptPresentation()
        pass
    pass

# Verify the platform:
def CheckPlatform() -> int:
    if not sys.platform.startswith('linux'):
        print("This script can only be used on Linux OS!")
        if not bDebugScript:
            return -1
        else:
            print("[DEBUG_MODE]::THIS SCRIPT IS EXECUTING IN DEBUG MODE!")
            return 1
    return 0

# Analyze the Command Line:
def CheckCommandLine() -> None:
    global bCtrlShowHelp
    global bVerboseMode

    # Verify the argument list:
    argI = 0
    argLower = ""
    argvSize = len(sys.argv)
    for arg in sys.argv:
        argLower = ""
        argLower = arg.lower()

        if bDebugScript:
            print(arg)
            pass

        if argLower == "-verbose":
            bVerboseMode = True
            pass

        if argLower == helpCmd[0] or argLower == helpCmd[1] or argLower == helpCmd[2] or len(sys.argv) == 1:
            bCtrlShowHelp = True
            pass

        # Control the arg index:
        argI = argI + 1
    pass

# -------------------------------- Script starts here -------------------------------- #

if __name__ == "__main__":
    exit(0)
else:
    exit(-1)