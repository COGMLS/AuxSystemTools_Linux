#pragma once

#ifndef FSTAB_TOOLS_HPP
#define FSTAB_TOOLS_HPP

#include <array>
#include <vector>
#include <string>
#include <cstring>
#include <fstream>
#include <memory>

#include "../Common/FileTools.hpp"
#include "../Common/ToolExceptions.hpp"

#include "DevDefines.hpp"
#include "MountPoint.hpp"

namespace LnxImgBack
{
	/**
	 * @brief Get the mount points that will be automatically mounted by the OS when boot
	 * @param mountPoints Vector of mount points
	 * @return 0 when successfull recover the information.
	 * @return 1 when no information was extracted from FSTAB file
	 */
	int getAutoMountPoints(std::vector<LnxImgBack::mount_point>& mountPoints);

	/**
	 * @brief Extract and format the data into a vector of arrays with specific fields
	 * @note The array index is the same for FSTAB file: 0 - disk uuid path, 1 - mount point, 2 - filesystem type, 3 - options, 4 - dump option, 5 - pass option
	 */
	std::vector<std::array<std::string, 6>> extractFsTabFileInfo();

	/**
	 * @brief Extract the FSTAB file line information, cutting the empty spaces and separating them in a vector to make easier to select the data
	 * @param line File line
	 * @return vector of selected string data
	 */
	std::vector<std::string> extractLineInfo(std::string line);
}

#endif // !FSTAB_TOOLS_HPP