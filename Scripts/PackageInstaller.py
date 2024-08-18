import os
import sys
import time

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   1,
        "Minor"     :   7,
        "Revision"  :   0
    }

# Configuration Version support:
__ConfigVersionSupport__ = 2

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
    "\nPackage Installer Script for Linux OS",
    "PARAMETERS:",
    "\t-PackList\tPaths to package files (Only configuration files (.ini))",
    "\t-Install\tDefine to install the packages, otherwise the packages will not been installed",
    "\t-Test\t\tTest the packages that will be installed",
    "\t-NewPackList\tCreate a new package list",
    "\t-Delay #\tCreate a delay between packages installations in seconds",
    "\t-Debug\tEnable the debug script",
    "\t-Experimental\tEnable the experimental features (may not work as specked)",
    "\nEXAMPLES:",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>...",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>... -Install",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>... -Test",
]

# Experimental Mode Warning Message:
ExperimentalModeWarning = "/!\\ WARNING::The script is under experimental mode!"

# Package Installer versioned file pattern:
class packageFilePatternV2:
    # Package File Pattern v.2 control variables:
    __minVersion__ = 1
    __maxVersion__ = 0 # Zero means no maximum version number
    __description__ = ""
    __config__ = ""
    __value__ = ""

    def __init__(self, description, configName, defaultValue="", minVersion=1, maxVersion=0) -> None:
        self.__description__ = description
        self.__configName__ = configName
        self.__configValue__ = defaultValue
        self.__minVersion__ = minVersion
        self.__maxVersion__ = maxVersion
        pass

    def isConfigVersionOk(self) -> bool:
        if self.__minVersion__ <= __ConfigVersionSupport__ and self.__maxVersion__ == 0:
            return True
        elif self.__minVersion__ <= __ConfigVersionSupport__ and self.__maxVersion__ >= __ConfigVersionSupport__:
            return True
        else:
            return False
        pass

    def getDescription(self) -> str:
        return self.__description__

    def getConfig(self) -> str:
        return self.__config__

    def getValue(self) -> str:
        return self.__value__

# Package Installer file pattern:
packageFilePattern = [
    "#Package Version: determinate if can use newer features or not. NOTE: The version number is only accepted integers and equal or greater than one. Otherwise, it will throw a program exception."
    "version=1"
    "# Package Manager Command: (example: yum, apt, apt-get, dnf, etc)",
    "packMng=",
    "# Package Manager Parameters: (example: --assume-yes)",
    "# NOTE: For each parameter, use space between then like console command line",
    "packMngParams=",
    "# Set 1 to use sudo or 0 to disable (NOTE: do not use space after equal)",
    "useSudo=",
    "# Add all packages to install. One by line."
]

# DEBUG the Script
# This constant is only for development and internal test purposes. To test the script without changing it, use the -debug parameter
DEBUG_SCRIPT = False

# Enable EXPERIMENTAL features in this script
# Experimental Mode for Development environment. This constant is only for used for development purposes, if you want use experimental feature, use -experimental parameter
EXPERIMENTAL_MODE_DEV = False

# Constants:
SCRIPT_DEFAULT_DELAY_INSTALL = 1

# Control variables:
bExperimentalMode = EXPERIMENTAL_MODE_DEV   # Determinate if will use the Experimental Features
bIsPackFileListChk = False
bIsPackFileListOk = False
bCtrlPackFileListTestPass = False
bCtrlInstall = False
bCtrlTest = False
bCtrlNewPackList = False
bCtrlShowHelp = False
bCtrlDelayInstall = False
ctrlDelayInstall = 1        # Delay between installations is disabled (in seconds)
bDebugScript = DEBUG_SCRIPT # Control the debug script.

# Check for Debug and Experimental mode parameters:
if not bDebugScript or not bExperimentalMode:
    for arg in sys.argv:
        if arg.lower() == "-debug":
            bDebugScript = True
            pass
        if arg.lower() == "-experimental":
            bExperimentalMode = True
            pass
        pass
    pass

# Verify the platform:
if not sys.platform.startswith('linux'):
    print("This script can only be used on Linux OS!")
    if not bDebugScript:
        exit(1)
    else:
        print("[DEBUG_MODE]::THIS SCRIPT IS EXECUTING IN DEBUG MODE!")
        pass
    pass

# Package File List Path:
filePackageListPath = ""
packTmp = ""

# Package Manage List:
packMng = []

# Package class: contains the package information
class Package:
    # Data Variables:
    bNeedSudo = False
    packName = ""
    packParams = []
    
    # Additional parameters for package installation, need use the configuration file in version 2
    bUseOptionalParams = False
    optPackParams = []

    def __init__(self, packName, bNeedSudo = False, packParams = []) -> None:
        self.packName = packName
        self.bNeedSudo = bNeedSudo
        self.packParams = packParams
        self.bUseOptionalParams = False
        self.optPackParams = []
        pass

    # Get the package information if will use sudo
    def GetNeedSudo(self) -> bool:
        return self.bNeedSudo
    
    # Get the package name
    def GetName(self) -> str:
        return self.packName

    # Get the package parameters
    def GetParams(self) -> list[str]:
        return self.packParams
    
    # Get the optional parameters status
    def GetOptParamStatus(self) -> bool:
        return self.bUseOptionalParams
    
    # Set to use or not the optional parameters
    def SetOptParamStatus(self, bUseOptParam) -> None:
        self.bUseOptionalParams = bUseOptParam
        pass
    
    # Get the optional parameters
    def GetOptParams(self) -> list[str]:
        return self.optPackParams
    
    # Set the optional parameters
    def SetOptParams(self, optPackParams) -> None:
        # Experimental features:
        if bExperimentalMode:
            self.optPackParams = optPackParams

            if len(optPackParams) > 0 and self.optPackParams[0] != '':
                self.SetOptParamStatus(True)
                pass
            pass
        pass

# Package Manager class: contains the package manager details
class PackageMng:
    # Control Variables:
    bDelayInstall = False
    delayValue = SCRIPT_DEFAULT_DELAY_INSTALL

    # Data variables:
    bUseSudo = False
    packMng = ""
    packMngParams = []
    packsList = []

    # Additional parameters:
    bUseOptionalParams = False
    optPackMngParams = []

    # Methods:

    def __init__(self, packMngCmd, packMngParams, bUseSudo = False) -> None:
        self.bUseSudo = bUseSudo
        self.packMng = packMngCmd
        self.packMngParams = packMngParams
        self.packsList = []
        self.bUseOptionalParams = False
        self.optPackMngParams = []
        pass
    
    # Check if will use the Sudo command
    def GetUseSudo(self) -> bool:
        return self.bUseSudo
    
    # Get the package manager name
    def GetPackMng(self) -> str:
        return self.packMng

    # Get the parameters for package manager
    def GetPackParams(self) -> list[str]:
        return self.packMngParams
    
    # Get the optional parameters for package manager
    def GetOptPackMngParams(self) -> list[str]:
        return self.optPackMngParams
    
    # Get the optional parameter setting:
    def GetOptParamStatus(self) -> bool:
        return self.bUseOptionalParams
    
    # Set to use or not the optional parameters:
    def SetOptParamStatus(self, bUseOptPackMngParams) -> None:
        # Experimental features:
        if bExperimentalMode:
            self.bUseOptionalParams = bUseOptPackMngParams
            pass
        pass

    # Set the optional parameters for Package Manager
    def SetOptParams(self, listOptPackMngParams) -> None:
        # Experimental features:
        if bExperimentalMode:
            self.optPackMngParams = listOptPackMngParams

            if len(self.optPackMngParams) > 0 and self.optPackMngParams[0] != '':
                self.SetOptParamStatus(True)
                pass
            pass
        pass

    # Get the list of packages that will be installed
    def GetPackList(self) -> list[Package]:
        return self.packsList
    
    # Add a list of packages to install
    def AddPackList(self, packList) -> None:
        self.packsList += packList
        pass
    
    # Add an item to packages list to install
    def AddPackListItem(self, pack) -> None:
        self.packsList.append(pack)
        pass

    # Clean the packages list to install
    def ResetPackList(self) -> None:
        self.packsList.clear()
        pass

    # Get the command to install a package
    def GetCommand(self, index) -> str:
        if len(self.packsList) > 0:

            package = self.packsList[index]
            cmd = ""
            if self.bUseSudo:
                cmd = "sudo "
                pass

            cmd += self.packMng + " "

            i = 0
            iMax = len(self.packMngParams)

            if iMax > 0 and self.packMngParams[0] != '':
                for param in self.packMngParams:
                    cmd += param
                    if i < iMax:
                        cmd += " "
                        i += 1
                        pass
                    pass
                pass

            # EXPERIMENTAL FEATURE: Add optional parameters
            if self.bUseOptionalParams and bExperimentalMode:
                # Add a space between the mandatory commands and optional ones:
                if iMax > 0 and self.packMngParams[0] != '':
                    cmd += " "
                    pass
                
                # Same logic used in packMngParam:
                i = 0
                iMax = len(self.optPackMngParams)

                if iMax > 0 and self.optPackMngParams[0] != '':
                    for optParam in self.optPackMngParams:
                        cmd += optParam
                        if i < iMax:
                            cmd += " "
                            i += 1
                            pass
                        pass
                    pass
                pass
            # ------------ END OF EXPERIMENTAL FEATURE ------------ #

            cmd += package
            return cmd
        else:
            return ""
    
    # Install the packages
    def InstallPackages(self) -> None:
        i = 0
        iMax = len(self.packsList)
        for package in self.packsList:
            if i < iMax:
                cmd = self.GetCommand(i)
                if bDebugScript:
                    print("[DEBUG]::Installing package:",package)
                    print("[DEBUG]::Executing command:",cmd)
                    pass
                if sys.platform.startswith('linux'):
                    os.system(cmd)  # Execute the command
                    pass
                else:
                    print("[FAIL]::The packages only can be installed on Linux OS!")
                    pass
                
                if self.bDelayInstall:
                    time.sleep(self.delayValue)
                    pass
                pass
            i += 1
            pass
        pass

    # Test the packages to install
    def TestInstallPackages(self) -> None:
        i = 0
        iMax = len(self.packsList)
        for package in self.packsList:
            if i < iMax:
                cmd = self.GetCommand(i)
                print("[TEST_MODE]::Installing package:",package)
                print("[TEST_MODE]::Executing command:",cmd,"\n")
                pass
            i += 1
            pass
        pass

    # Define delay in seconds or disable it, using zero
    def setDelay(self, delay) -> None:
        if delay > 0:
            self.bDelayInstall = True
            self.delayValue = delay
            pass
        else:
            self.bDelayInstall = False
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

# Control variables to argument analysis:
ctrlArgs_TestDelayInstall = False
ctrlArgs_DelayPos = -1
ctrlArgs_FoundDelayArg = False

# Verify the argument list:
argI = 0
argLower = ""
for arg in sys.argv:
    argLower = ""
    argLower = arg.lower()

    if bDebugScript:
        print(arg)
        pass

    if bIsPackFileListOk and bIsPackFileListChk:
        bIsPackFileListChk = False
        filePackageListPath = arg
        pass

    if argLower == "-packlist" and not bIsPackFileListChk:
        bIsPackFileListOk = True
        bIsPackFileListChk = True
        pass

    if argLower == "-install":
        bCtrlInstall = True
        pass

    if argLower == "-test":
        bCtrlTest = True
        pass

    if argLower == "-newpacklist":
        bCtrlNewPackList = True
        pass

    if argLower == "-delay" and not ctrlArgs_FoundDelayArg:
        bCtrlDelayInstall = True
        ctrlArgs_TestDelayInstall = True
        ctrlDelayInstall = SCRIPT_DEFAULT_DELAY_INSTALL # To avoid a possible no more arguments to analyze, set the default value here
        ctrlArgs_DelayPos = argI
        ctrlArgs_FoundDelayArg = True
        pass

    if ctrlArgs_TestDelayInstall and argLower != "-delay":
        # 0: Correctly defined. 1: Delay parameter is not greater than zero. 2: Delay parameter doesn't have a digit. -1: An exception occur. -2: Delay parameter is empty.
        ctrlArgs_WarningForceDefaultDelay = 0

        # Test the arg length if exist a next argument for delay parameter:
        if len(sys.argv) > ctrlArgs_DelayPos + 1:
            argDelayValue = sys.argv[ctrlArgs_DelayPos + 1]

            # Test if the delay value is a number:
            try:
                # Try to convert the value:
                try:
                    argDelayValue = int(argDelayValue)
                except:
                    ctrlDelayInstall = SCRIPT_DEFAULT_DELAY_INSTALL
                    ctrlArgs_WarningForceDefaultDelay = 2

                # Test the value:
                if argDelayValue > 0 and ctrlArgs_WarningForceDefaultDelay == 0:
                    ctrlDelayInstall = argDelayValue
                    pass
                else:
                    ctrlDelayInstall = SCRIPT_DEFAULT_DELAY_INSTALL
                    ctrlArgs_WarningForceDefaultDelay = 1
                    pass
            except:
                ctrlDelayInstall = SCRIPT_DEFAULT_DELAY_INSTALL
                ctrlArgs_WarningForceDefaultDelay = -1
            pass
        else:
            ctrlArgs_WarningForceDefaultDelay = -2
            pass

        # Treat the delay parameter warning messages:
        if ctrlArgs_WarningForceDefaultDelay == 0 and bDebugScript:
            print("The delay parameter was defined. Using the value: ",ctrlDelayInstall," s.")
            pass
        elif ctrlArgs_WarningForceDefaultDelay == 1:
            print("The delay parameter was not defined as a number greater than zero! Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
        elif ctrlArgs_WarningForceDefaultDelay == 2:
            print("The delay parameter doesn't have a number. Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
            pass
        elif ctrlArgs_WarningForceDefaultDelay == -1:
            print("An exception occur during the delay value processing. Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
            pass
        else:
            print("The delay parameter is empty. Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
            pass

        # Show debug information about delay parameter:
        if bDebugScript:
            print("Error code: ",ctrlArgs_WarningForceDefaultDelay,"\n")
            pass
        else:
            print("\n")
            pass

        ctrlArgs_TestDelayInstall = False   # Disable ctrlArgs_TestDelayInstall after check.
        pass

    if argLower == helpCmd[0] or argLower == helpCmd[1] or argLower == helpCmd[2] or len(sys.argv) == 1:
        bCtrlShowHelp = True
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

# Create the a new package file list:
if bCtrlNewPackList:
    newPathFilePath = os.path.realpath(__file__).replace(sys.argv[0],"NewPackList.ini")

    try:
        newFileObj = open(newPathFilePath, 'x')

        for lp in packageFilePattern:
            lp = lp + "\n"
            newFileObj.write(lp)
            pass

        newFileObj.close()
    except FileExistsError:
        print("The file already exist!\nFilePath: ",newPathFilePath)
    except:
        print("Fail to create the file!")

    exit(0)
    pass

# Test the package file list:
if bIsPackFileListOk:
    filePackageListPath = filePackageListPath.split(',')

    for packTmp in filePackageListPath:

        # Verify if the pack files has double quotes to avoid path tests errors:
        if packTmp.startswith('"'):
            packTmp = packTmp.removeprefix('"')
            pass
        if packTmp.endswith('"'):
            packTmp = packTmp.removesuffix('"')
            pass

        if bDebugScript:
            print("[DEBUG]::Package file status:")
            print("[DEBUG]::File: ",packTmp)
            print("[DEBUG]::Exists: ",os.path.exists(packTmp))
            pass

        if os.path.exists(packTmp):
            bCtrlPackFileListTestPass = True
            if bDebugScript:
                exceptionStr = "Found the Package File List (" + packTmp + ")"
                print(exceptionStr)
                pass

            fileObj = open(packTmp, 'r')

            cfgFileVersion = 1  # Assume 1 if the configuration version is not set in the file

            bUseSudo = False
            packMngName = ""
            packMngParams = []
            packs2Install = []

            # EXPERIMENTAL FEATURE: Verify the configuration file for version support
            optPackMngParams = []

            if bExperimentalMode:
                vStr = ""
                for l in fileObj.readlines():
                    if l.startswith("version="):
                        vLine = l.split('=')
                        vStr = vLine[1]
                        break
                    pass

                # Test if the value is a number:
                if vStr.isdigit():
                    # Test if the version number is compatible with the script:
                    if vStr >= 1 and vStr <= __ConfigVersionSupport__:
                        cfgFileVersion = vStr
                        pass
                    pass

                # Go back to the begin of the file
                fileObj.seek(0)

                pass
            # ------------------- END OF EXPERIMENTAL FEATURE --------------------- #

            # Read and interpret the file:
            for l in fileObj.readlines():
                bIsComment = False

                # Verify for commented lines:
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

                # In case the line is not a comment, interpret it
                if len(l) > 0 and not bIsComment:
                    l = l.replace('\n','')
                    if l.__contains__("packMng="):
                        packMngName = l.split('=')[1]

                        if bDebugScript:
                            print("packMngName:",packMngName)
                            pass
                        pass
                    elif l.__contains__("packMngParams="):
                        lTmp = l.split('=')
                        packMngParams = lTmp[1].split(' ')

                        if bDebugScript:
                            print("packMngParams:",packMngParams)
                            pass
                        pass
                    # EXPERIMENTAL FEATURE: Verify the existence of optPackMngParams:
                    elif l.__contains__("optPackMngParams=") and bExperimentalMode:
                        lOptTmp = l.split('=')
                        optPackMngParams = lOptTmp[1].split(' ')

                        if bDebugScript:
                            print("optPackMngParams:",optPackMngParams)
                            pass
                        pass
                    # --------------- END OF EXPERIMENTAL FEATURE ----------------- #
                    elif l.__contains__("useSudo=1"):
                        bUseSudo = True

                        if bDebugScript:
                            print("useSudo:",bUseSudo)
                            pass
                        pass
                    elif l.__contains__("useSudo=0"):
                        bUseSudo = False

                        if bDebugScript:
                            print("useSudo:",bUseSudo)
                            pass
                        pass
                    else:
                        packs2Install.append(l)
                        pass
                    pass
                pass
            
            # Show the complete package list after read all lines (Only in Debug Mode):
            if bDebugScript:
                print("\nPackages to install:")
                i = 0
                for pck in packs2Install:
                    pckStr = "[" + i.__str__() + "]::" + pck
                    print(pckStr)
                    i = i + 1
                    pass
                print("")
                pass

            fileObj.close()

            packMngObj = PackageMng(packMngName, packMngParams, bUseSudo)

            packMngObj.AddPackList(packs2Install)

            if bCtrlDelayInstall:
                packMngObj.setDelay(ctrlDelayInstall)
                pass

            packMng.append(packMngObj)
            pass
        else:
            print("Fail to detect the Package File List (",packTmp,")")
            pass
        pass
else:
    print("The Package File List wasn't defined!","\nPackList: ",filePackageListPath)
    exit(2)

# Create the packages founded on files in CLI:
for m in packMng:
    if bCtrlInstall and bCtrlTest:
        print("Can't use -Install and -Test parameters at the same time!")
        pass
    elif bCtrlInstall and not bCtrlTest:
        print("\nInstalling packages with: ",m.GetPackMng())
        print("Package Manager Parameters: ",m.GetPackParams())
        print("Using SUDO: ",m.bUseSudo,"\n")
        m.InstallPackages()
        pass
    elif not bCtrlInstall and bCtrlTest:
        print("\nInstalling packages with: ",m.GetPackMng())
        print("Package Manager Parameters: ",m.GetPackParams())
        print("Using SUDO: ",m.GetUseSudo(),"\n")
        m.TestInstallPackages()
        pass
    else:
        print(m)
        pass

    # Fast delay between package files:
    if bCtrlDelayInstall:
        time.sleep(SCRIPT_DEFAULT_DELAY_INSTALL)
        pass
    pass
