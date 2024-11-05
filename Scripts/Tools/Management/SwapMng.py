import os
import sys
import shutil
import psutil
import enum

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   0,
        "Minor"     :   4,
        "patch"     :   0
    }

# Help command line:
helpCmd = ["--help","-h","-?"]

# Help info:
help = [
    "\nDefault Swap file Manager for Linux (SwapMng)",
    "PARAMETERS:",
    "\t-a --add\tAdd the swap default file. (Only will take effect if does not exist)",
    "\t-r --remove\tRemove the default file. (Only will take effect if does exist)",
    "\t-c --change\tMake changes in default swap file (swap.img), only if exist.",
    "\t-s --size\tSize for modify or create the swap file.",
    "\nEXPERIMENTAL PARAMETERS:",
    "\t-e --enable\tEnable a registered swap",
    "\t-u --unable\tUnable a registerd swap",
    "\t-p --path\tComplete swap file path",
    "\t-d --default\tUse default (/swap.img) swap file",
    "\n\t\tTo use a specific parameter help, use <param> -? or <param> -h or <param> --help\n",
    "\nCONTROL PARAMETERS:",
    "\t--experimental\tEnable the experimental features",
    "\t--debug\tDebug the script and make no changes in the system"
]

help_params = {
        "add":[
            "Add Swap File:",
            "\t -a --add",
            "\t\tCreate and register a swap file in fstab file",
            "\tExamples:\n",
            "Add the default swap file (/swap.img) with size 8G:",
            "\tsudo python SwapMng.py --add --default --size 8G",
            "Add a swap file using --path parameter with 10G:",
            "\tsudo python SwapMng.py --add --path /customPath/mySwapFile.img --size 10G"
        ],
        "remove":[
            "Remove Swap File:",
            "\t -r --remove",
            "\t\tRemove and unregister a swap file in fstab file",
            "\tExamples:\n",
            "Remove the default swap file (/swap.img):",
            "\tsudo python SwapMng.py --remove --default",
            "Remove a swap file using --path parameter:",
            "\tsudo python SwapMng.py --remove --path /customPath/mySwapFile.img"
        ],
        "change":[
            "Change the Swap File size:",
            "\t -c --change",
            "\t\tModifies the swap file.",
            "\t\tIf the file does not exist, it will be created and registered",
            "\tExamples:\n",
            "Modify the default swap file size to 16G (/swap.img):",
            "\tsudo python SwapMng.py --change --default --size 16G",
            "Modify a swap file size to 8G using --path parameter:",
            "\tsudo python SwapMng.py --change --path /customPath/mySwapFile.img --size 8G"
        ],
        "size":[
            "Size paramter:",
            "\t -s --size <size>",
            "Define the file size. The size can be used with a letter to represent:",
            "\tK - kilobyte",
            "\tM - megabyte",
            "\tG - gigabyte"
            "If no letter is used with the size number, it will be in bytes.",
            "\tExamples:\n",
            "Create the default swap file with 8 gigabytes:",
            "\tsudo python SwapMng.py --add --default --size 8G",
            "Modify the default swap file to 1500 megabytes (NOTE: Carefull setting a low size swap file)",
            "\tsudo python SwapMng.py --change --default --size 1500M"
        ],
        "enable":[

        ],
        "unable":[

        ],
        "path":[

        ],
        "default":[

        ],
        "experimental":[

        ],
        "debug":[

        ]
    }

# Experimental Mode Warning Message:
ExperimentalModeWarning = "/!\\ WARNING::The script is under experimental mode!"

# Datatypes:

class ParamData:
    __param__ = ""
    __data__ = ""

    def __init__(self, param, data) -> None:
        self.__param__ = param
        self.__data__ = data
        pass

    def getParam(self) -> str:
        return self.__param__
    
    def getData(self) -> str:
        return self.__data__
    
class SizeMag(enum):
    b   = 512,
    kB  = 1000,
    K   = 1024,
    MB  = 1000*1000,
    M   = 1024*1024,
    GB  = 1000*1000*1000,
    G   = 1024*1024*1024

class Size:
    size = 0
    mag = SizeMag.b
    bSizeOk = False
    bMagOk = False

    def __init__(self, size: str) -> None:
        number = ""
        mag = ""
        for c in size:
            if c.isdigit():
                number = number + c
                pass
            else:
                mag = mag + c
                pass
            pass

        try:
            number = int(number)
            self.bSizeOk = True
        except:
            self.bSizeOk = False

        match mag:
            case "b":
                self.mag = SizeMag.b
                self.bMagOk = True
            case "kB":
                self.mag = SizeMag.kB
                self.bMagOk = True
            case "K":
                self.mag = SizeMag.K
                self.bMagOk = True
            case "MB":
                self.mag = SizeMag.MB
                self.bMagOk = True
            case "M":
                self.mag = SizeMag.M
                self.bMagOk = True
            case "GB":
                self.mag = SizeMag.GB
                self.bMagOk = True
            case "G":
                self.mag = SizeMag.G
                self.bMagOk = True
            case _:
                self.bMagOk = False
        pass

    def getSize(self) -> int:
        if self.bSizeOk and self.bMagOk:
            return self.size
        else:
            return -1

    def getTotalSize(self) -> int:
        if self.bSizeOk and self.bMagOk:
            return self.size * int(self.mag)
        else:
            return -1

    def getMag(self) -> SizeMag:
        return self.mag
    
    def isSizeOk(self) -> bool:
        return self.bMagOk and self.bSizeOk

# Constants:

DEBUG_SCRIPT = True
ENABLE_EXPERIMENTAL_FEATURES = True
DEFAULT_SWAP_FILE_PATH = "/swap.img"
FSTAB_FILE_PATH = "/media/mlsma/Apps-Media/Projetos/GitRepos/AuxSystemTools_Linux/Temp/fstab"
FSTAB_FILE_PATH_BACKUP = "/media/mlsma/Apps-Media/Projetos/GitRepos/AuxSystemTools_Linux/Temp/fstab.back"

#FSTAB_FILE_PATH = "/etc/fstab"
#FSTAB_FILE_PATH_BACKUP = "/temp/fstab.back"

# Internal variables:

bDebugScript = DEBUG_SCRIPT
bExperimentalMode = ENABLE_EXPERIMENTAL_FEATURES
bShowHelp = False
bIsCliOk = False
bUseDefaultSwapFile = False
params = [ParamData]

# Parameter control variables:

usedAddParam = 0
usedRemoveParam = 0
usedChangeParam = 0
usedDefaultParam = 0
usedPathParam = 0
usedSizeParam = 0

# Script's functions:

# Print the script version:
def PrintScriptVersion() -> str:
    strVer = "v."
    strVer += __ScriptVersionNumber__["Major"].__str__()
    strVer += "."
    strVer += __ScriptVersionNumber__["Minor"].__str__()
    strVer += "."
    strVer += __ScriptVersionNumber__["patch"].__str__()
    return strVer

def show_help(helpCmd = "") -> None:
    if helpCmd == "":
        pass
    else:

        pass
    pass

# Remove command line parameters
def ResolveCmdLineParams() -> list[ParamData]:
    _list = list[ParamData]

    # Make sure the used parameters are not recalculated if this method is called more than one time:

    usedAddParam = 0
    usedRemoveParam = 0
    usedChangeParam = 0
    usedDefaultParam = 0
    usedPathParam = 0
    usedSizeParam = 0

    # Method start here:

    foundChangeSizeParam = 0
    foundRemoveParam = 0
    foundAddParam = 0
    foundSizeParam = 0
    foundPathParam = 0

    param = ""
    data = ""

    for arg in sys.argv:
        if arg.startswith('-'):
            param = ""
            data = ""
            arg = arg.lower()
            # Test for debug:
            if arg == "--debug":
                bDebugScript = True
                param = "debug"
                paramObj = ParamData(param, "")
                _list.append(paramObj)
                pass
            # Enable experimental features:
            if arg == "--experimental":
                bExperimentalMode = True
                param = "experimental"
                paramObj = ParamData(param, "")
                _list.append(paramObj)
                pass
            # Check for help command:
            for j in help:
                if arg == j:
                    bShowHelp = True
                    break
                pass
            # Change size:
            if arg == "--change" or arg == "-c":
                foundChangeSizeParam = 2
                param = "change"
                paramObj = ParamData(param, data)
                _list.append(paramObj)
                usedChangeParam = usedChangeParam + 1
                pass
            # Add param:
            if arg == "--add" or arg == "-a":
                foundAddParam = 2
                param = "add"
                paramObj = ParamData(param, data)
                _list.append(paramObj)
                usedAddParam = usedAddParam + 1
                pass
            # Remove param:
            if arg == "--remove" or arg == "-r":
                foundRemoveParam = 2
                param = "remove"
                paramObj = ParamData(param, data)
                _list.append(paramObj)
                usedRemoveParam = usedRemoveParam + 1
                pass
            # Size:
            if arg == "--size" or arg == "-s":
                foundSizeParam = 1
                param = "size"
                usedSizeParam = usedSizeParam + 1
                pass
            # Path param:
            if arg == "--path" or arg == "-p":
                foundPathParam = 1
                param = "path"
                usedPathParam = usedPathParam + 1
                pass
            # Default param:
            if arg == "--default" or arg == "-d":
                param = "default"
                paramObj = ParamData(param, "")
                _list.append(paramObj)
                usedDefaultParam = usedDefaultParam + 1
                pass
            pass
        else:
            # Try to get the new size:
            if foundSizeParam == 1 and foundRemoveParam != 1 and foundAddParam != 1 and foundChangeSizeParam != 1 and foundPathParam != 1:
                data = arg
                foundSizeParam = 2
                paramObj = ParamData(param, data)
                _list.append(paramObj)
                pass
            # Try to get the path:
            if foundSizeParam != 1 and foundRemoveParam != 1 and foundAddParam != 1 and foundChangeSizeParam != 1 and foundPathParam == 1:
                data = arg
                foundPathParam = 2
                paramObj = ParamData(param, data)
                _list.append(paramObj)
                pass
            pass
        pass

    return _list

# Verify if the parameters was used only one time and if no incompatible parameter was combined:
def VerifyParams() -> int:
    status = 0

    # Test if the parameters was used only one time:
    if usedAddParam > 1 or usedChangeParam > 1 or usedRemoveParam > 1 or usedDefaultParam > 1 or usedPathParam > 1 or usedSizeParam > 1:
        status = status + 1
        pass

    # Test if --add, --change and/or --remove was combined:
    if (usedAddParam and usedChangeParam) or (usedAddParam and usedChangeParam) or (usedChangeParam and usedRemoveParam) or (usedAddParam and usedChangeParam and usedRemoveParam):
        status = status + 2
        pass

    # Test if --default and --path was combined:
    if usedDefaultParam and usedPathParam:
        status = status + 4
        pass

    # Test if --size and --remove was combined:
    if usedSizeParam and usedRemoveParam:
        status = status + 8
        pass

    return status

# Add a swap file
def AddSwapFile(path: str, size: str) -> int:
    status = 0

    # If the file already exist:
    if os.path.exists(path):
        return -1

    _size = Size(size)

    _count = str(_size.getSize())
    _bs = str(_size.getMag())

    cmdList = [
        f"sudo dd if=/dev/zero of={path} bs={_bs} count={_count}",
        f"sudo chmod 0600 {path}",
        f"sudo mkswap {path}",
        f"sudo swapon {path}"
    ]

    i = 1
    iMax = len(cmdList)

    while i < iMax:
        if bDebugScript:
            print(f"[DEBUG]::[COMMAND]::{cmdList[i]}")
            pass
        else:
            j = os.system(cmdList[i])

            if j != 0:
                status = i  # Determinate the line of command list that failed
                break
            pass
        pass

    return status

# Remove a swap file
def RemoveSwapFile(path) -> int:
    status = 0

    if not os.path.exists(path):
        return -1

    cmdList = [
        f"sudo swapoff {path}",
        f"sudo rm {path}"
    ]

    i = 1
    iMax = len(cmdList)

    while i < iMax:
        if bDebugScript:
            print(f"[DEBUG]::[COMMAND]::{cmdList[i]}")
            pass
        else:
            j = os.system(cmdList[i])

            if j != 0:
                status = i  # Determinate the line of command list that failed
                break
            pass
        pass

    return status

# Change a swap file
def ChangeSwapFile(path, size) -> int:
    status = 0

    status = AddSwapFile(path, size)

    # If the file already exist, try to remove:
    if status == -1:
        status = RemovePersistentSwap(path)
        pass

    status = AddSwapFile(path, size)

    return status

# Read the fstab file
def Read_fstab_File() -> list[str]:
    fstabContent = [str]

    fstab = open(FSTAB_FILE_PATH, "r")
    for l in fstab:
        fstabContent.append(l)
        pass
    fstab.close()

    return fstabContent

# Save the changes in fstab file
def Save_fstab_File(fstab: list[str]) -> int:
    status = 0

    # Make a backup copy:
    if os.path.exists(FSTAB_FILE_PATH_BACKUP):
        os.remove(FSTAB_FILE_PATH_BACKUP)
        pass

    shutil.copy(FSTAB_FILE_PATH, FSTAB_FILE_PATH_BACKUP)

    # Write the lines into the fstab file:

    fstabFile = open(FSTAB_FILE_PATH, "w+")

    if fstabFile.writable():
        i = 1
        iMax = len(fstab)

        while i < iMax:
            try:
                l = fstab[i]
                if not l.endswith('\n') and i + 1 < iMax:
                    l = l + '\n'
                    pass
                fstabFile.write(l)
            except:
                status = 2
            i = i + 1
            pass
    else:
        status = 1
        pass

    fstabFile.close()

    return status

# Make the swap persistent
def MakePersistentSwap(fstab: list[str], path: str, mountpoint: str, type: str, options: str, bDump: str, bPass: str) -> list[str]:
    status = 0
    bHasLine = False
    i = 1
    iMax = len(fstab)

    while i < iMax:
        if fstab[i].__contains__(path):
            bHasLine = True
            break
        i = i + 1
        pass

    line = f"{path}\t{mountpoint}\t{type}\t{options}\t{bDump}\t{bPass}"

    if bHasLine:
        fstab[i] = line
        pass
    else:
        fstab.append(line)
        pass

    return fstab

# Remove persistent swap
def RemovePersistentSwap(fstab: list[str], path: str) -> list[str]:
    status = 0
    bRemovedLine = False

    for l in fstab:
        try:
            if l.__contains__(path):
                fstab.remove(l)
                bRemovedLine = True
                pass
        except:
            status = 2
        pass

    if status == 0 and not bRemovedLine:
        status = 1
        pass

    return fstab

# Unable a persistent swap
def UnablePersistentSwap(fstab: list[str], path: str) -> list[str]:
    status = 0
    bFoundLine = False
    i = 1
    iMax = len(fstab)

    while i < iMax:
        if fstab[i].__contains__(path):
            fstab[i] = "# " + fstab[i]
            break
        i = i + 1
        pass

    return fstab

# Enable a persistent swap
def EnablePersistentSwap(fstab: list[str], path: str) -> list[str]:
    status = 0
    bFoundLine = False
    i = 1
    iMax = len(fstab)

    while i < iMax:
        if fstab[i].__contains__(path):
            bFoundLine = True
            break
        i = i + 1
        pass

    if bFoundLine:
        if fstab[i].startswith("# "):
            fstab[i] = fstab[i].removeprefix("# ")
            pass
        pass

    return fstab

# Verify the fstab file for persistent filesystems swap files.
# If return 0, none swap path was found.
# If return 1, found a enabled swap file.
# If return 2, found an unable swap file.
def SwapPersistentStatus(fstab: list[str], path: str) -> int:
    status = 0

    i = 1
    iMax = len(fstab)

    while i < iMax:
        l = fstab[i]
        if l.__contains__(path):
            if l.startswith("# "):
                status = 2
                break
            else:
                status = 1
                break
            pass
        pass

    return status

# Test the platform and the user rights:

if not sys.platform.startswith('linux'):
    print("This script is only for Linux OS")
    exit(1)

if os.getuid() != 0 and not bDebugScript:
    print("[FAIL]::The script is not running with super user rights!")
    exit(2)

if bShowHelp:
    pass

# Swap Manager (SwapMng) start here:

if bExperimentalMode:
    if os.path.exists(FSTAB_FILE_PATH):
        os.remove(FSTAB_FILE_PATH)
        pass
    shutil.copy(FSTAB_FILE_PATH_BACKUP, FSTAB_FILE_PATH)

    fstabfile = Read_fstab_File()
    print(f"FSTAB CONTENT:\n{fstabfile}")
    fstabfile = RemovePersistentSwap(fstabfile, "/dev/disk/by-uuid/FDA3-86BD")
    fstabfile = MakePersistentSwap(fstabfile, "/myswap.img", "none", "swap", "sw", "0", "0")
    print(f"FSTAB CONTENT:\n{fstabfile}")
    UnablePersistentSwap(fstabfile, "/swap.img")
    EnablePersistentSwap(fstabfile, "/boot/efi")
    save_status = Save_fstab_File(fstabfile)
    print(f"Save Status: {save_status}")

    pass