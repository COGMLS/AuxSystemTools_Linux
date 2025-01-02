#pragma once

#ifndef VERSION_INFORMATION_HPP
#define VERSION_INFORMATION_HPP

#include <string>
#include <cstring>

#include "Version.hpp"

namespace LnxImgBack
{
	/**
	 * @brief Version data
	 */
	struct Version
	{
		unsigned int major;
		unsigned int minor;
		unsigned int patch;
		unsigned long long build;
		unsigned int revision;
		char* type;
	};

	/**
	 * @brief Get the version data
	 * @return Return a Version struct
	 */
	inline LnxImgBack::Version getLibVersion()
	{
		LnxImgBack::Version v;
		v.major = LINUX_IMAGE_BACKUP_TOOL_MAJOR_VERSION;
		v.minor = LINUX_IMAGE_BACKUP_TOOL_MINOR_VERSION;
		v.patch = LINUX_IMAGE_BACKUP_TOOL_PATCH_VERSION;
		v.build = LINUX_IMAGE_BACKUP_TOOL_BUILD_NUMBER;
		v.revision = LINUX_IMAGE_BACKUP_TOOL_BUILD_TYPE_NUMBER;
		std::strcpy(v.type, LINUX_IMAGE_BACKUP_TOOL_BUILD_TYPE);
		return v;
	}

	/**
	 * @brief Transform the struct Version into a string version
	 * @param version Version struct
	 * @param showBuild Show the build number.
	 * @param showType Show the build type.
	 * @return Return a string version.
	 */
	inline std::string getVersionStr (LnxImgBack::Version version, bool showBuild, bool showType)
	{
		std::string s;
		s = std::to_string(version.major) + "." + std::to_string(version.minor) + "." + std::to_string(version.patch);

		if (showType && !(std::strcmp(version.type, "release") == 0 || std::strcmp(version.type, "RELEASE") == 0))
		{
			s += "-" + std::string(version.type);
		}

		if (version.revision > 0)
		{
			s += "." + std::to_string(version.revision);
		}

		if (showBuild)
		{
			s += " build " + std::to_string(version.build);
		}

		return s;
	}
}

#endif // !VERSION_INFORMATION_HPP