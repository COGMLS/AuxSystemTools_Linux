#include "SysTools.hpp"

std::string LnxImgBack::getHostName()
{
	return std::getenv("HOSTNAME");
}

std::string LnxImgBack::getUserName()
{
    return std::getenv("USER");
}

int LnxImgBack::hasRootRights()
{
	bool isSystemCred = false;      // Detect if the user is using system credentials (as sudo)
    bool isForcedSysOp = false;     // Detect if is a system operation

	uid_t me = getuid();
    uid_t myPrivileges = geteuid();

    // If the current user is running with other user credentials and is not root, send a error message
    if (me != myPrivileges && me != 0)
    {
        return -1;
    }

    return 0;
}
