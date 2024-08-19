import os
import sys
import time

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   1,
        "Minor"     :   1,
        "Revision"  :   3
    }

# Debug Script mode:
DEBUG_SCRIPT = False

# Control Variables:
bDebugScript = DEBUG_SCRIPT
bVerboseMode = False
bLegacyMode = True
bUpdate = True
bConfirmChanges = False
bCtrlShowHelp = False
bRunAsAdmin = False
bCheckOnly = False
bDebugCmdTask = False
bUseExceptList = False
bUseAllExceptList = False
bNewConfigFile = False
bListConfig = False
bListConfigPriority = False

taskExcept = []

# Global configurations for UpdateSystem.py
CONFIG_EXTENSION = ".ini"
LOCAL_CONFIG = os.getenv("HOME") + "/.config/AuxSystemTools/UpdateSystem"
LOCAL_CONFIG_EXCEPTLIST = LOCAL_CONFIG + "/ExceptList"

# Help command line:
helpCmd = ["-help","-h","-?"]

# Help info:
help = [
    "\nUpdate System script for Linux OS",
    "PARAMETERS:",
    "\tNOTE: All parameters with '*' in their description has a specific notes about how they work.",
    "\t-help | -h | -?\tShow the script help",
    "\t-Legacy\tUse legacy system update operations.\n\t\tThis method need you edit this script to make new tasks.",
    "\t-DebugScript\tEnable the script debug",
    "\t-DebugCmd\tEnable the debug mode for a specific tool*",
    "\t-Check\tOnly verify if there are updates available*",
    "\t-Update\tAllow to apply automatically the updates*",
    "\t-Except [All | configName1,...]\tUse exception lists available in configuration files.\n\t\tUsing 'All' will assume to all configuration files that has a exception list.\n\t\tOtherwise use the config. name (for more than one, use comma to separate).",
    "\t-NewConfig [name]\tCreate a new configuration file with a specific name.\n\t\tYou need to set the commands and package names to make it work.",
    "\t-ListConfig\tList all configuration files available.",
    "\t-ListTaskOrder\tList the task orders. Will show the highest priority to lowest.",
    "\n\nNOTES:",
    "\t* All commands with '*' will only will execute the configurations that was successfully detected the internal settings.\n\t\tIf a configuration fail in the validation process, the script will show a warning message.",
]

configFilePattern = [
    "# Define the settings to use the UpdateSystem.py",
    "# All comments should be start with '#' and are only accepted on begging of the line.",
    "# Avoid use spaces in configurations. It may lead to unexpected behaviors.",
    "version=1",
    "[ToolDefinitions]",
    "# Define the command to call the tool for update",
    "cmd=",
    "# Common parameters used in all operations. Use the term '<PackList>' to define an specific location to UpdateSystem add the packages to update. By default the UpdateSystem add the package list in the end.",
    "commonParams=",
    "# Set 1 to use sudo in all operations, 2 only in update tasks",
    "sudo=",
    "# Set specific command to confirm automatically the operation",
    "confirmArg=",
    "# Set specific command to automatically negate the operation",
    "negateArg=",
    "# Set the command to only check for updates (NOTE: if this command for this tool doesn't need sudo privileges, set sudo=2 or sudo=0)",
    "checkArg=",
    "# Define the command to debug the tool",
    "debugArg=",
    "# Set the verbose argument for the tool",
    "verboseArg=",
    "# Set the exception list files available in ~/.config/AuxSystemTools/UpdateSystem/ExceptList to be used with this tool",
    "# Exception lists holds package names one by line!",
    "# Use comma to separate the exception lists",
    "exceptListAllowed="
]

# Check for Debug parameter:
if not bDebugScript:
    for arg in sys.argv:
        if arg.lower() == "-debugscript":
            bDebugScript = True
            break
        pass
    pass

# Check the configuration files and exception list directories. If the directory does not exist, create it:
def CheckConfigDirectory(configPath: str) -> int:
    if os.path.exists(configPath):
        return 0

    try:
        os.makedirs(configPath)
        return 0
    except:
        return 1
    pass

# Get the configuration files and return a list:
def GetConfigFilesList(path: str) -> list:
    filesList = []
    for i in os.listdir(path):
        if os.path.isfile(i):
            filesList.append(i)
            pass
        pass
    return filesList

# Create a new configuration file for the user
def CreateNewConfigFile(configName: str) -> int:
    # Create the a new package file list:
    newPathFilePath = LOCAL_CONFIG + f"/{configName}" + CONFIG_EXTENSION

    try:
        newFileObj = open(newPathFilePath, 'x')

        for l in configFilePattern:
            l = l + "\n"
            newFileObj.write(l)
            pass

        newFileObj.close()
        return 0
    except FileExistsError:
        print(f"The file already exist!\nFilePath: {newPathFilePath}")
        return 1
    except:
        print("Fail to create the file!")
        return 2
    pass

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

# Legacy tasks method:
def runLegacyTasks():
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

    print("\nUpdating system packages...\n")
    time.sleep(5.0)

    UpdateSys(packMng, "upgrade")

    UpdateSnap()

    UpdateSys(packMng, "autoremove")
    #UpdateSys(packMng, "clean --packages")

    print("\nDone!\n")
    pass

# -------------------------------- Analyse the command line ------------------------------ #

ctrlArgs_FoundExceptArg = False
#ctrlArgs_ExceptPos = -1
ctrlArgs_FoundNewConfigFileArg = False
ctrlArgs_NewConfigFileName = ""

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

    if argLower == "-legacy":
        bLegacyMode = True
        pass

    if argLower == "-update":
        bConfirmChanges = True
        pass

    if argLower == "-check":
        bCheckOnly = True
        pass

    if argLower == "-debugcmd":
        bDebugCmdTask = True
        pass

    if ctrlArgs_FoundExceptArg and argLower != "-except":
        if argvSize > 2:
            lastArg = sys.argv[argI - 1].lower()
            if lastArg == "-except":
                if argLower == "all":
                    bUseAllExceptList = True
                    pass
                else:
                    exceptListStr = lastArg.split(',')
                    pass
                pass
            pass
        else:
            # Fail to get the exception list
            pass
        ctrlArgs_FoundExceptArg = False # Disable the search for exception lists when done.
        pass

    if argLower == "-except" and not ctrlArgs_FoundExceptArg:
        bUseExceptList = True
        ctrlArgs_FoundExceptArg = True
        pass
    
    if argLower == "-newconfig" and not ctrlArgs_FoundNewConfigFileArg:
        bNewConfigFile = True
        ctrlArgs_FoundNewConfigFileArg = True
        pass

    if argLower != "-newconfig" and ctrlArgs_FoundNewConfigFileArg:
        if argvSize > 2:
            lastArg = sys.argv[argI - 1].lower()
            if lastArg == "-newconfig":
                # Verify if the configuration's name contains a possible character that is not allowed:
                if argLower.startswith('-') or argLower.__contains__('/') or argLower.__contains__('\\'):
                    # Not a valid name
                    pass
                else:
                    ctrlArgs_NewConfigFileName = sys.argv[argI]
                    pass
                pass
            else:
                # Fail to get the new config file's name
                pass
            pass
            ctrlArgs_NewConfigFileName = False  # Disable the search for new configuration file name when done.
        pass

    if argLower == "-listconfig":
        bListConfig = True
        pass

    if argLower == "-listtaskorder":
        bListConfigPriority = True
        pass

    if argLower == helpCmd[0] or argLower == helpCmd[1] or argLower == helpCmd[2] or len(sys.argv) == 1:
        if not bLegacyMode:
            bCtrlShowHelp = True
            pass
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

time.sleep(2)

# -------------- Analyze the control variables and the system environment --------------- #

# Verify the platform:
if not sys.platform.startswith('linux'):
    print("This script is only for Linux OS")
    exit(1)

# Verify the user id:
if os.getuid() != 0 and not DEBUG_SCRIPT and bLegacyMode:
    print("[FAIL]::The script is not running with super user rights!")
    exit(2)

if bNewConfigFile:
    if ctrlArgs_NewConfigFileName != "":
        CreateNewConfigFile(ctrlArgs_NewConfigFileName)
        exit(0)
        pass
    else:
        exit(3)

# Enter on list mode:
if bListConfig or bListConfigPriority:
    if bListConfig:
        pass
    if bListConfigPriority:
        pass
    exit(0)

# Not allowed to use update and check together
if bCheckOnly and bUpdate:
    exit(4)

# --------------------------------- The script starts here ------------------------------- #

# Run legacy or new mode:
if bLegacyMode:
    runLegacyTasks()
    pass
else:
    # Test first the directories:
    if CheckConfigDirectory(LOCAL_CONFIG) != 0:
        pass
    if CheckConfigDirectory(LOCAL_CONFIG_EXCEPTLIST) != 0:
        pass
    pass

exit(0)