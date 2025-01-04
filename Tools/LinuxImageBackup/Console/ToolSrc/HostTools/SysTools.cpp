#include "SysTools.hpp"

std::string LnxImgBack::getHostName()
{
	return std::getenv("HOSTNAME");
}

std::string LnxImgBack::getUserName()
{
    return std::getenv("USER");
}

bool LnxImgBack::hasRootRights()
{
	uid_t me = getuid();

    if (me == 0)
    {
        return true;
    }

    return false;
}
