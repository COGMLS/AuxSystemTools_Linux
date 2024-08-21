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
maxCfgVersionSupported = 1          # Determinate the maximum version number for configuration files

taskExceptList = []

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
    #"\t-NewExceptList [name]\tCreate a new exception list with a specific name.\n\t\tYou need to set the package names. If the a empty list if loaded, it will be ignored."
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
    "# Use comma to separate the exception lists names. Eg. exceptListAllowed=nokernel,firefox",
    "exceptListAllowed="
]

exceptListPattern = [
    "# Exception List for UpdateSystem.py",
    "# Use one package name by line to determinate the packages this list will hold to avoid a update task",
    "# Do not change the file 's name or it's extension or move from ExceptList directory.",
    "# The exception list is identified by it's name.",
    "# Do not use '#' as first character in line or will be considered as a commented line!"
]

# Check for Debug parameter:
if not bDebugScript:
    for arg in sys.argv:
        if arg.lower() == "-debugscript":
            bDebugScript = True
            break
        pass
    pass

# Class to create manageable object that can apply the custom tasks
class UpdateTask:
    # Control variables:
    __name__ = ""               # Task name
    __filepath__ = ""           # Task configuration's file path
    __isValidTask__ = False     # Task validation variable
    __version__ = 1             # Task version for config. file

    __sudoCmdType__ = 0
    __bHasCmd__ = False
    __bHasConfirmParam__ = False
    __bHasNegateParam__ = False
    __bHasCheckParam__ = False
    __bHasVerboseParam__ = False
    __bHasDebugParam__ = False
    __bUseExceptList__ = False

    __cmd__ = ""                # Command line tool that wil be called to perform an specific action
    __commonParams__ = []       # Parameters used in both task methods: update and check. If a <PackList> is identified in common parameters, will insert in this location the package list for exceptions. Otherwise will add in the end of the common parameter list.
    __confirmParam__ = ""       # Command used to automate the confirmation like -y or --assumeyes or any other with the same behavior
    __negateParam__ = ""        # Command used to negate a task like -n or --assumeno or other parameters with the same behavior
    __checkParam__ = ""         # A check only or verification parameter
    __debugParam__ = ""         # A single command tha can enable the debug on cmd tool
    __verboseParam__ = ""       # A single command that if used with the cmd to enable the verbose mode
    __allowedExceptList__ = []  # Holds the base names of all exception lists
    __exceptList__ = []         # Holds the path os all lists that was available in allowedExceptList and match with filterList

    # Internal methods:

    # Filter the Except List available with all lists that exist in the LOCAL_CONFIG_EXCEPTLIST and match with the user entry:
    def __filter_except_list__(self, filterList: list[str]) -> None:
        lExceptList = list[str]
        if len(self.__allowedExceptList__) > 0:
            if os.path.exists(LOCAL_CONFIG_EXCEPTLIST):
                exceptFiles = os.listdir(LOCAL_CONFIG_EXCEPTLIST)
                for excFile in exceptFiles:
                    if os.path.isfile(excFile) and excFile.endswith(CONFIG_EXTENSION):
                        if self.__allowedExceptList__.__contains__(os.path.basename(excFile).removesuffix(CONFIG_EXTENSION)):
                            lExceptList.append(excFile)
                            pass
                        pass
                    pass
                pass
            pass

        if len(filterList) > 0 and len(lExceptList) > 0:
            for i in filterList:
                if lExceptList.__contains__(i):
                    self.__exceptList__.append(i)
                    pass
                pass
            pass
        pass

    # Get the exception packages inside a exception file:
    def __get_except_packages__(self, exceptFile: str) -> list[str]:
        lExceptList = list[str]
        try:
            file = open(exceptFile, 'r')

            for l in file.readlines():
                bIsComment = False

                if len(l) > 0 and l != "":
                    i = 0
                    iMax = len(l)
                    bIsValidChar = False
                    while i < iMax:
                        if l[i] == ' ':
                            pass
                        elif l[i] == '#' and not bIsValidChar:
                            bIsComment = True
                            break
                        else:
                            bIsValidChar = True
                            break
                        i = i + 1
                        pass

                    if not bIsComment:
                        lExceptList.append(l)
                        pass
                    pass
                pass
            pass
        except:
            if bDebugScript:
                print(f"[DEBUG]::[TASK - {self.__name__}]::Fail to get the packages in {exceptFile}")
                pass
            pass
        return lExceptList

    def __organize_param_list__(self, paramList: list[str]) -> list[str]:
        lParamList = list[str]

        return lParamList

    # Methods:

    def __init__(self, configFilePath: str, exceptList: list[str]) -> None:
        self.__filepath__ = configFilePath
        if os.path.exists(configFilePath):
            try:
                self.__name__ = os.path.basename(configFilePath)
                self.__name__ = self.__name__.removesuffix(CONFIG_EXTENSION)
                
                file = open(self.__filepath__, 'r')
                
                cfgFileVersion = 1  # If no version file was defined, assume 1.

                # Search for version file:
                vLine = list[str]
                for l in file.readlines():
                    if l.startswith("version="):
                        vLine = l.split('=')
                        break
                        pass
                    pass

                # Test if version field has a value and if it's equal or higher than 1 and equal or lower than maxCfgVersionSupported
                if len(vLine) > 1:
                    if vLine[1].isdigit():
                        if vLine[1] >= 1 and vLine[1] <= maxCfgVersionSupported:
                            cfgFileVersion = vLine[1]
                        pass
                    pass

                self.__version__ = cfgFileVersion

                # Reset the file position to read for all configuration fields:
                file.seek(0)

                # Read all other fields, based on version:
                for l in file.readlines():
                    bIsComment = False

                    # Look for commented lines:
                    if len(l) > 0:
                        i = 0
                        iMax = len(l)
                        bIsValidChar = False
                        while i < iMax:
                            if l[i] == ' ':
                                pass
                            elif l[i] == '#' and not bIsValidChar:
                                bIsComment = True
                                break
                            else:
                                bIsValidChar = True
                                break
                            i = i + 1
                            pass
                        pass
                    pass

                    # In case the line is not a comment, interpret it:
                    if len(l) > 0 and not bIsComment:
                        l = l.replace('\n','')

                        # Configuration field interpreter for versions 1 and higher:
                        if self.__version__ >= 1:

                            # Check for command value:
                            if l.startswith("cmd="):
                                vList = l.split('=')
                                if len(vList) > 1:
                                    self.__cmd__ = vList[1]
                                    self.__bHasCmd__ = True
                                    pass
                                else:
                                    self.__isValidTask__ = False
                                    if bVerboseMode:
                                        print(f"Fail to create the task. {self.__name__}.")
                                        pass
                                    if bDebugScript:
                                        print(f"[DEBUG]::Fail to create a valid task because the configuration cmd field is not valid.")
                                        pass
                                    pass
                                pass

                            # Check for common parameters:
                            if l.startswith("commonParams="):
                                l = l.removeprefix("commonParams=")
                                vList = l.split(' ')
                                if len(vList) > 0:
                                    self.__commonParams__ = vList
                                    pass
                                pass

                            # Check for sudo command type:
                            if l.startswith("sudo="):
                                l = l.removeprefix("sudo=")
                                bSudoTypeDefined = False
                                if len(l) > 0 and l != "":
                                    if l.isdigit():
                                        if l >= 0 and l <= 2:
                                            self.__sudoCmdType__ = l
                                            bSudoTypeDefined = True
                                            pass
                                        else:
                                            print(f"[TASK - {self.__name__}]::The sudo value definition is not recognized by this configuration version!")
                                            pass
                                        pass
                                    pass

                                if not bSudoTypeDefined:
                                    if os.getuid() == 0:
                                        self.__sudoCmdType__ = 1
                                        pass
                                    if bVerboseMode or bDebugScript:
                                        print(f"[TASK - {self.__name__}]::Sudo wasn't defined on configuration file, assuming the execution user credentials!")
                                        pass
                                    pass
                                pass

                            # Check for confirmation argument value:
                            if l.startswith("confirmArg="):
                                l = l.removeprefix("confirmArg=")
                                if len(l) > 0 and l != "":
                                    self.__confirmParam__ = l
                                    self.__bHasConfirmParam__ = True
                                    pass
                                pass

                            # Check for negate argument value:
                            if l.startswith("negateArg="):
                                l = l.removeprefix("negateArg=")
                                if len(l) > 0 and l != "":
                                    self.__negateParam__ = l
                                    self.__bHasNegateParam__ = True
                                    pass
                                pass

                            # Check for a checking or verification argument value:
                            if l.startswith("checkArg="):
                                l = l.removeprefix("checkArg=")
                                if len(l) > 0 and l != "":
                                    self.__checkParam__ = l
                                    self.__bHasCheckParam__ = True
                                    pass
                                pass

                            # Check for debug tool argument value:
                            if l.startswith("debugArg="):
                                l = l.removeprefix("debugArg=")
                                if len(l) > 0 and l != "":
                                    self.__debugParam__ = l
                                    self.__bHasDebugParam__ = True
                                    pass
                                pass

                            # Check for verbose argument value:
                            if l.startswith("verboseArg="):
                                l = l.removeprefix("verboseArg=")
                                if len(l) > 0 and l != "":
                                    self.__verboseParam__ = l
                                    self.__bHasVerboseParam__ = True
                                    pass
                                pass

                            # Check for a allowed exception list:
                            if l.startswith("exceptListAllowed="):
                                l = l.removeprefix("exceptListAllowed=")
                                vList = l.split(',')
                                if len(vList) > 0:
                                    self.__allowedExceptList__ = vList
                                    pass
                                pass
                            pass
                        pass
                    pass

                # Organize the exception lists available:
                if len(exceptList) > 0:
                    self.__filter_except_list__(exceptList)
                    pass

                # Show the object information if verbose and/or debug script is enabled:
                if bVerboseMode:
                    print(f"[TASK - {self.__name__}]::Created with configuration file {configFilePath}")
                    pass
                if bDebugScript:
                    print(f"[DEBUG]::The object task was created, using the reference configuration file {configFilePath}")
                    print(f"[DEBUG]::Object variables:")
                    print(f"Name:{self.__name__}")
                    print(f"Version:{self.__version__}")
                    print(f"Command [{self.__bHasCmd__}]:{self.__cmd__}")
                    print(f"CommonParams:{self.__commonParams__}")
                    print(f"ConfirmParam [{self.__bHasConfirmParam__}]:{self.__confirmParam__}")
                    print(f"NegateParam [{self.__bHasNegateParam__}]:{self.__negateParam__}")
                    print(f"CheckParam [{self.__bHasCheckParam__}]:{self.__checkParam__}")
                    print(f"VerboseParam [{self.__bHasVerboseParam__}]:{self.__verboseParam__}")
                    print(f"DebugParam [{self.__bHasDebugParam__}]:{self.__debugParam__}")
                    print(f"AllowedExceptList:{self.__allowedExceptList__}")
                    print(f"ExceptList:{self.__exceptList__}")
                    pass
                pass
            except:
                if bVerboseMode:
                    print(f"Fail to create the task for {configFilePath}")
                    pass
                if bDebugScript:
                    print(f"[DEBUG]::The object task creation fail using the reference configuration file {configFilePath}")
                    print(f"[DEBUG]::Object variables:")
                    print(f"Name:{self.__name__}")
                    print(f"Version:{self.__version__}")
                    print(f"Command [{self.__bHasCmd__}]:{self.__cmd__}")
                    print(f"CommonParams:{self.__commonParams__}")
                    print(f"ConfirmParam [{self.__bHasConfirmParam__}]:{self.__confirmParam__}")
                    print(f"NegateParam [{self.__bHasNegateParam__}]:{self.__negateParam__}")
                    print(f"CheckParam [{self.__bHasCheckParam__}]:{self.__checkParam__}")
                    print(f"VerboseParam [{self.__bHasVerboseParam__}]:{self.__verboseParam__}")
                    print(f"DebugParam [{self.__bHasDebugParam__}]:{self.__debugParam__}")
                    print(f"AllowedExceptList:{self.__allowedExceptList__}")
                    print(f"ExceptList:{self.__exceptList__}")
                    pass
                pass
            pass
        else:
            self.__isValidTask__ = False
            if bVerboseMode:
                print(f"The configuration file {configFilePath} doesn't exist!")
                pass
            if bDebugScript:
                print(f"[DEBUG]::Fail to create a valid task with configuration file {configFilePath}")
                pass
            pass
        pass

    def getName(self) -> str:
        return self.__name__
    
    def getFilepath(self) -> str:
        return self.__filepath__
    
    def getSudoStatus(self) -> int:
        return self.__sudoCmdType__
    
    def getCmd(self) -> str:
        return self.__cmd__
    
    def getCommonParams(self) -> list[str]:
        return self.__commonParams__
    
    def getConfirmParam(self) -> str:
        return self.__confirmParam__
    
    def getNegateParam(self) -> str:
        return self.__negateParam__
    
    def getVerboseParam(self) -> str:
        return self.__verboseParam__
    
    def getDebugParam(self) -> str:
        return self.__debugParam__
    
    def getExceptList(self) -> list[str]:
        return self.__allowedExceptList__
    
    def getUsedExceptions(self) -> list[str]:
        return self.__exceptList__
    
    def isTaskOk(self) -> bool:
        return self.__isValidTask__

    # Task Methods:

    def Update(self) -> int:
        pass

    def Check(self) -> int:
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

# Create a new script supported file for the user
def CreateNewScriptFile(filename: str, filetype: int) -> int:
    if filetype == 0:
        # Create the a new package file list:
        newPathFilePath = LOCAL_CONFIG + f"/{filename}" + CONFIG_EXTENSION
        filePattern = configFilePattern
        pass
    elif filetype == 1:
        # Create a new exception file:
        newPathFilePath = LOCAL_CONFIG_EXCEPTLIST + f"/{filename}" + CONFIG_EXTENSION
        filePattern = exceptListPattern
        pass
    else:
        raise Exception(f"File pattern type not recognized! Used type: {filetype}")
        pass

    try:
        newFileObj = open(newPathFilePath, 'x')

        for l in filePattern:
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
                    taskExceptList = lastArg.split(',')
                    pass
                pass
            pass
        else:
            # Fail to get the exception list. Assume to use all exception lists available.
            print("NO SPECIFIC EXCEPTION BEHAVIOR WAS DEFINED! ASSUMING ALL EXCEPTION LISTS AVAILABLE.")
            bUseAllExceptList = True
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
                    print("The file name can not have the characters: '/', '\\' or start with '-'.")
                    exit(6)
                    pass
                elif argLower == "all":
                    # If "all" was used as a configuration file name
                    print("The file name 'all' can not be used for a configuration file, because is a keyword to specify all exception lists!")
                    exit(7)
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
        else:
            break
            pass
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
        if CreateNewScriptFile(ctrlArgs_NewConfigFileName, 0) == 0:
            print(f"Created the configuration file: {LOCAL_CONFIG}/{ctrlArgs_NewConfigFileName}{CONFIG_EXTENSION}")
            exit(0)
        else:
            print(f"Fail to create the configuration file: {LOCAL_CONFIG}/{ctrlArgs_NewConfigFileName}{CONFIG_EXTENSION}")
            exit(5)
    else:
        print("Fail to create the configuration file. A name for the configuration is needed.")
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
    print("Using -Update and -Check parameters  is not allowed.")
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