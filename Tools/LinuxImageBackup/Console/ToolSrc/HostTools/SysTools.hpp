#pragma once

#ifndef SYSTEM_TOOLS_HPP
#define SYSTEM_TOOLS_HPP

#include <string>
#include <cstdlib>
#include <unistd.h>

namespace LnxImgBack
{
	/**
	 * @brief Wrapper to return the hostname
	 */
	std::string getHostName();

	/**
	 * @brief Wrapper to return the actual username
	 */
	std::string getUserName();

	int hasRootRights();
}

#endif // !SYSTEM_TOOLS_HPP