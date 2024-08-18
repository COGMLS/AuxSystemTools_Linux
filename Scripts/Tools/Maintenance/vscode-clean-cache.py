import os
import sys
import time
import shutil

# ----------------------- SCRIPT PLATFORM, COMMAND LINE, DEBUG AND EXPERIMENTAL MODE VERIFICATIONS ------------------------- #

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   0,
        "Minor"     :   1,
        "Revision"  :   0
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

# Help command line:
helpCmd = ["-help","-h","-?"]

# Help info:
help = [
    "\nVisual Studio Code maintenance script for Linux OS"
]

# Experimental Mode Warning Message:
ExperimentalModeWarning = "/!\\ WARNING::The script is under experimental mode!"

# DEBUG the Script
# This constant is only for development and internal test purposes. To test the script without changing it, use the -debug parameter
DEBUG_SCRIPT = False

# Constants:
SCRIPT_DEFAULT_DELAY_INSTALL = 2

# Control variables:
bExperimentalMode = False   # Determinate if will use the Experimental Features
bPrintInfo = True
bVerboseMode = True
bConfirmOp = False
bTestMode = False
bCtrlShowHelp = False
bDebugScript = DEBUG_SCRIPT  # Control the debug script.

# Check for Debug and Experimental parameters:
if not bDebugScript:
    for arg in sys.argv:
        if arg.lower() == "-debug":
            bDebugScript = True
            pass

        if arg.lower() == "-experimental":
            bExperimentalMode = True
            pass
        pass
    pass

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
    print(help[0]," - ",PrintScriptVersion())
    print(line)

    # Show the debug mode message if is in DEBUG MODE:
    if bDebugScript:
        print("DEBUG MODE ENABLED")
        pass

    # Show the experimental mode warning:
    if bExperimentalMode:
        print(ExperimentalModeWarning)
        time.sleep(SCRIPT_DEFAULT_DELAY_INSTALL * 2)
        pass

    time.sleep(SCRIPT_DEFAULT_DELAY_INSTALL)
    pass

# Verify the platform:
if not sys.platform.startswith('linux'):
    print("This script can only be used on Linux OS!")
    if not bDebugScript:
        exit(1)
    #else:
    #    print("[DEBUG_MODE]::THIS SCRIPT IS EXECUTING IN DEBUG MODE!")
    #    pass
    pass

# Verify the argument list:
argI = 0
argLower = ""
for arg in sys.argv:
    argLower = ""
    argLower = arg.lower()

    if bDebugScript:
        print(arg)
        pass

    if argLower == "-verbose":
        pass

    if argLower == "-confirm":
        pass

    if argLower == "-test":
        pass

    if argLower == helpCmd[0] or argLower == helpCmd[1] or argLower == helpCmd[2] or len(sys.argv) == 1:
        #bCtrlShowHelp = True
        break
        pass

    # Control the arg index:
    argI = argI + 1

# Test if there is no argument
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

# ----------------- SCRIPT START HERE ----------------- #

# -----------------------------------------------------
# Visual Studio Code paths on Linux:
# -----------------------------------------------------
# cpp-extension: ~/.cache/vscode-cpptools
# Code Config: ~/.config/Code
# NOTE: The user settings.json and keybindings.json are located in ~/.config/Code/User
# Code Extensions: ~/.vscode
# print-extension: ~/.vscode-print-resource-cache
# -----------------------------------------------------

vscodePaths = [
    "~/.config/Code",
    "~/.cache/vscode-cpptools"
]

vscodePath2Save = [
    f"{vscodePaths[0]}/User/settings.json",
    f"{vscodePaths[0]}/User/keybindings.json",
    f"{vscodePaths[0]}/User",
]

tempSaveRoot = "/tmp/vscode-clean-cache"

# Contains the information about the object path
class infoPath:
    exist = False
    name = ""
    path = ""
    isFile = ""

    def __init__(self, name, path, isFile, exist) -> None:
        self.exist = exist
        self.name = name
        self.path = path
        self.isFile = isFile
        pass

    def printInfo(self) -> None:
        print(f"Name: {self.name}")
        print(f"Path: {self.path}")
        basePath = self.path.removesuffix("/" + self.name)
        print(f"Basepath: {basePath}")
        print(f"IsFile: {self.isFile}")
        print(f"Exist: {self.exist}")
        pass

# Files and directories that will be moved into a temporary directory
class savedPaths:
    bPathExist = False
    bIsFile = False
    name = ""
    originalPath = ""
    currentPath = ""

    def __changePath__(self, newPath: str) -> None:
        self.currentPath = newPath
        pass

    def __init__(self, path: str) -> None:
        homePath = os.getenv("HOME")

        self.originalPath = path

        if self.originalPath.startswith("~"):
            self.originalPath = self.originalPath.replace("~", homePath)
            pass

        self.currentPath = self.originalPath
        self.bPathExist = os.path.exists(self.originalPath)
        self.name = os.path.basename(self.originalPath)
        self.bIsFile = os.path.isfile(self.currentPath)
        pass

    def getInfo(self) -> infoPath:
        return infoPath(self.name, self.currentPath, self.bIsFile, self.bPathExist)
        pass

    def move2Tmp(self) -> bool:
        try:
            if not os.path.exists(tempSaveRoot):
                if bVerboseMode:
                    print(f"Creating temporary directory {tempSaveRoot}...")
                    pass
                if not bTestMode:
                    os.makedirs(tempSaveRoot)
                    pass
                pass
            if self.bIsFile:
                if bVerboseMode:
                    print(f"Moving file {self.name} to temp directory...")
                    pass
                if not bTestMode:
                    newPath = shutil.move(self.currentPath, os.path.join(tempSaveRoot, self.name))
                    self.__changePath__(newPath)
                    pass
                pass
            else:
                if bVerboseMode:
                    print(f"Moving directory {self.name} to temp directory...")
                    pass
                if not bTestMode:
                    newPath = shutil.copytree(self.currentPath, os.path.join(tempSaveRoot, self.name))
                    self.__changePath__(newPath)
                    pass
                pass
            return True
        except:
            return False
            pass
        pass

    def move2OriginalPath(self) -> bool:
        try:
            if self.bIsFile:
                basePath = self.originalPath.removesuffix(self.name)

                if not os.path.exists(basePath):
                    if bVerboseMode:
                        print(f"Recreating the original directory structure {basePath}...")
                        pass
                    if not bTestMode:
                        os.makedirs(basePath)
                        pass
                    pass

                if bVerboseMode:
                    print(f"Restoring the file {self.name} location...")
                    pass

                if not bTestMode:
                    newPath = shutil.move(self.currentPath, self.originalPath)
                    self.__changePath__(newPath)
                    pass
                pass
            else:
                if bVerboseMode:
                    print(f"Restoring the directory {self.name} location...")
                    pass
                if not bTestMode:
                    newPath = shutil.copytree(self.currentPath, self.originalPath)
                    self.__changePath__(newPath)
                    pass
                pass
            return True
        except:
            return False
            pass
        pass

item2Save = []

i = 0
for j in vscodePath2Save:
    obj = savedPaths(j)
    if bPrintInfo:
        obj.getInfo().printInfo()
        print("")
        pass
    item2Save.insert(i, obj)
    i += 1
    pass

#i = 0
#iMax = len(item2Save)
#for item in item2Save:
#    if i < iMax:
#        o = item.getInfo()
#        o.printInfo()
#        print("")
#        pass
#    i += 1
#    pass