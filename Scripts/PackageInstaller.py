import os
import sys

# Verify the platform:
if not sys.platform.startswith('linux'):
    print("This script can only be used on Linux OS!")
    exit(1)

# DEBUG the Script
DEBUGSCRIPT = True

# Control variables:
bIsPackFileListChk = False
bIsPackFileListOk = False
bCtrlPackFileListTestPass = False
bCtrlInstall = False
bCtrlTest = False

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
        pass
    
    def GetUseSudo(self) -> bool:
        return self.bUseSudo
    
    def GetPackMng(self) -> str:
        return self.packMng

    def GetPackParams(self) -> list[str]:
        return self.packMngParams
    
    def GetPackList(self) -> list[Package]:
        return self.packsList
    
    def AddPackList(self, packList) -> None:
        self.packsList += packList
        pass
    
    def AddPackListItem(self, pack) -> None:
        self.packsList.append(pack)
        pass

    def ResetPackList(self) -> None:
        self.packsList.clear()
        pass

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

    def TestInstallPackages(self) -> None:
        i = 0
        iMax = len(self.packsList)
        for package in self.packsList:
            if i < iMax:
                cmd = self.GetCommand(i)
                if DEBUGSCRIPT:
                    print("[TEST_MODE]::Installing package:",package)
                    print("[TEST_MODE]::Executing command:",cmd)
                    pass
                pass
            i += 1
            pass
        pass

# Verify the argument list:
for arg in sys.argv:
    if DEBUGSCRIPT:
        print(arg)
        pass

    if bIsPackFileListOk and bIsPackFileListChk:
        bIsPackFileListChk = False
        filePackageListPath = arg
        pass

    if arg == "-PackList" and not bIsPackFileListChk:
        bIsPackFileListOk = True
        bIsPackFileListChk = True
        pass

    if arg == "-Install":
        bCtrlInstall = True
        pass

    if arg == "-Test":
        bCtrlTest = True
        pass

# Test the package file list:
if bIsPackFileListOk:
    filePackageListPath = filePackageListPath.split(',')

    for packTmp in filePackageListPath:
        if os.path.exists(packTmp):
            bCtrlPackFileListTestPass = True
            if DEBUGSCRIPT:
                print("Found the Package File List (",packTmp,")")
                pass

            fileObj = open(packTmp, 'r')

            bUseSudo = False
            packMngName = ""
            packMngParams = []
            packs2Install = []

            for l in fileObj.readlines():
                if len(l) > 0:
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

                        if DEBUGSCRIPT:
                            print("To packs2Install:",l)
                            pass
                        pass
                    pass
                pass

            fileObj.close()

            packMngObj = PackageMng(packMngName, packMngParams, bUseSudo)

            for pck in packs2Install:
                packMngObj.AddPackListItem(pck)
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
