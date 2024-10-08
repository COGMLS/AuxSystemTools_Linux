import os
import sys
import time

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   1,
        "Minor"     :   6,
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
    "\t-Debug\tEnable the debug script"
    "\nEXAMPLES:",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>...",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>... -Install",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>... -Test",
]

# Package Installer file pattern:
packageFilePattern = [
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
DEBUGSCRIPT = False

# Constants:
SCRIPT_DEFAULT_DELAY_INSTALL = 1

# Control variables:
bIsPackFileListChk = False
bIsPackFileListOk = False
bCtrlPackFileListTestPass = False
bCtrlInstall = False
bCtrlTest = False
bCtrlNewPackList = False
bCtrlShowHelp = False
bCtrlDelayInstall = False
ctrlDelayInstall = 1        # Delay between installations is disabled (in seconds)
bDebugScript = DEBUGSCRIPT  # Control the debug script.

# Check for Debug parameter:
if not bDebugScript:
    for arg in sys.argv:
        if arg.lower() == "-debug":
            bDebugScript = True
            break
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

# Package class: contains the package informations
class Package:
    # Data Variables:
    bNeedSudo = False
    packName = ""
    packParams = []

    def __init__(self, packName, bNeedSudo = False, packParams = []) -> None:
        self.packName = packName
        self.bNeedSudo = bNeedSudo
        self.packParams = packParams
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

    # Methods:

    def __init__(self, packMngCmd, packMngParams, bUseSudo = False) -> None:
        self.bUseSudo = bUseSudo
        self.packMng = packMngCmd
        self.packMngParams = packMngParams
        self.packsList = []
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
    arglower = arg.lower()

    if bDebugScript:
        print(arg)
        pass

    if bIsPackFileListOk and bIsPackFileListChk:
        bIsPackFileListChk = False
        filePackageListPath = arg
        pass

    if arglower == "-packlist" and not bIsPackFileListChk:
        bIsPackFileListOk = True
        bIsPackFileListChk = True
        pass

    if arglower == "-install":
        bCtrlInstall = True
        pass

    if arglower == "-test":
        bCtrlTest = True
        pass

    if arglower == "-newpacklist":
        bCtrlNewPackList = True
        pass

    if arglower == "-delay" and not ctrlArgs_FoundDelayArg:
        bCtrlDelayInstall = True
        ctrlArgs_TestDelayInstall = True
        ctrlDelayInstall = SCRIPT_DEFAULT_DELAY_INSTALL # To avoid a possible no more arguments to analyze, set the default value here
        ctrlArgs_DelayPos = argI
        ctrlArgs_FoundDelayArg = True
        pass

    if ctrlArgs_TestDelayInstall and arglower != "-delay":
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
            print("The delay parameter was apllied. Using the value: ",ctrlDelayInstall," s.")
            pass
        elif ctrlArgs_WarningForceDefaultDelay == 1:
            print("The delay parameter was not defined as a number greater than zero! Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
        elif ctrlArgs_WarningForceDefaultDelay == 2:
            print("The delay parameter doens't have a number. Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
            pass
        elif ctrlArgs_WarningForceDefaultDelay == -1:
            print("An exception occur during the delay value processing. Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
            pass
        else:
            print("The delay parameter is empty. Using the default value: ",SCRIPT_DEFAULT_DELAY_INSTALL," s")
            pass

        # Show debug informations about delay parameter:
        if bDebugScript:
            print("Error code: ",ctrlArgs_WarningForceDefaultDelay,"\n")
            pass
        else:
            print("\n")
            pass

        ctrlArgs_TestDelayInstall = False   # Disable ctrlArgs_TestDelayInstall after check.
        pass

    if arglower == helpCmd[0] or arglower == helpCmd[1] or arglower == helpCmd[2] or len(sys.argv) == 1:
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

            bUseSudo = False
            packMngName = ""
            packMngParams = []
            packs2Install = []

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
