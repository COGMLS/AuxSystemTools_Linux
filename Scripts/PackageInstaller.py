import os
import sys

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   1,
        "Minor"     :   5,
        "Revision"  :   18
    }

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
    "\nEXAMPLES:",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>...",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>... -Install",
    "\tPackageInstaller.py -PackList <PackListFile1Path.txt>,<PackListFile2Path.txt>... -Test",
]

# Package Installer file pattern:
packageFilePattern = [
    "# Package Manager Command: (example: yum, apt, apt-get, etc)",
    "packMng=",
    "# Package Manager Parameters: (example: --assume-yes)",
    "# NOTE: For each parameter, use space between then like console command line",
    "packMngParams=",
    "# Set 1 to use sudo or 0 to disable (NOTE: do not use space after equal)",
    "useSudo=",
    "# Add all packages to install. One by line."
]

# DEBUG the Script
DEBUGSCRIPT = True

# Verify the platform:
if not sys.platform.startswith('linux'):
    print("This script can only be used on Linux OS!")
    if not DEBUGSCRIPT:
        print("[DEBUG_MODE]::THIS SCRIPT IS EXECUTING IN DEBUG MODE!")
        exit(1)
    pass

# Control variables:
bIsPackFileListChk = False
bIsPackFileListOk = False
bCtrlPackFileListTestPass = False
bCtrlInstall = False
bCtrlTest = False
bCtrlNewPackList = False
bCtrlShowHelp = False

# Package File List Path:
filePackageListPath = ""
packTmp = ""

# Package Manage List:
packMng = []

# Package class: contains the package informations
class Package:
    bNeedSudo = False
    packName = ""
    packParams = []

    def __init__(self, packName, bNeedSudo = False, packParams = []) -> None:
        self.packName = packName
        self.bNeedSudo = bNeedSudo
        self.packParams = packParams
        pass

    def GetNeedSudo(self) -> bool:
        return self.bNeedSudo
    
    def GetName(self) -> str:
        return self.packName

    def GetParams(self) -> list[str]:
        return self.packParams

# Package Manager class: contains the package manager details
class PackageMng:
    bUseSudo = False
    packMng = ""
    packMngParams = []
    packsList = []

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

            if iMax > 0:
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
                if DEBUGSCRIPT:
                    print("[DEBUG]::Installing package:",package)
                    print("[DEBUG]::Executing command:",cmd)
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
    pass

# Verify the argument list:
for arg in sys.argv:
    arg = arg.lower()
    if DEBUGSCRIPT:
        print(arg)
        pass

    if bIsPackFileListOk and bIsPackFileListChk:
        bIsPackFileListChk = False
        filePackageListPath = arg
        pass

    if arg == "-packlist" and not bIsPackFileListChk:
        bIsPackFileListOk = True
        bIsPackFileListChk = True
        pass

    if arg == "-install":
        bCtrlInstall = True
        pass

    if arg == "-test":
        bCtrlTest = True
        pass

    if arg == "-newpacklist":
        bCtrlNewPackList = True
        pass

    if arg == helpCmd[0] or arg == helpCmd[1] or arg == helpCmd[2] or len(sys.argv) == 1:
        bCtrlShowHelp = True
        break
        pass

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
        if os.path.exists(packTmp):
            bCtrlPackFileListTestPass = True
            if DEBUGSCRIPT:
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

                        if DEBUGSCRIPT:
                            print("packMngName:",packMngName)
                            pass
                        pass
                    elif l.__contains__("packMngParams="):
                        lTmp = l.split('=')
                        packMngParams = lTmp[1].split(' ')

                        if DEBUGSCRIPT:
                            print("packMngParams:",packMngParams)
                            pass
                        pass
                    elif l.__contains__("useSudo=1"):
                        bUseSudo = True

                        if DEBUGSCRIPT:
                            print("useSudo:",bUseSudo)
                            pass
                        pass
                    elif l.__contains__("useSudo=0"):
                        bUseSudo = False

                        if DEBUGSCRIPT:
                            print("useSudo:",bUseSudo)
                            pass
                        pass
                    else:
                        packs2Install.append(l)
                        pass
                    pass
                pass
            
            # Show the complete package list after read all lines (Only in Debug Mode):
            if DEBUGSCRIPT:
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
        print("\nInstalling packages with: ",m.packMng)
        print("Package Manager Parameters: ",m.packMngParams)
        print("Using SUDO: ",m.bUseSudo,"\n")
        m.InstallPackages()
        pass
    elif not bCtrlInstall and bCtrlTest:
        print("\nInstalling packages with: ",m.packMng)
        print("Package Manager Parameters: ",m.packMngParams)
        print("Using SUDO: ",m.bUseSudo,"\n")
        m.TestInstallPackages()
        pass
    else:
        print(m)
        pass
    pass
