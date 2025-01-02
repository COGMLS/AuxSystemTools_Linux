#include <iostream>

#include "VersionInfo.hpp"

#include "Exception.hpp"
#include "ConsoleOutput.hpp"

int main (int argc, const char* argv[])
{
	std::cout << LnxImgBack::getVersionStr(LnxImgBack::getLibVersion(), true, true) << std::endl;
	return 0;
}