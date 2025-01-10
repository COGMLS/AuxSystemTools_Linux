#pragma once

#ifndef MOUNT_POINT_HPP
#define MOUNT_POINT_HPP

#include <string>
#include <cstring>
#include <filesystem>

#include "../Common/ToolExceptions.hpp"

#include "DevDefines.hpp"
#include "DeviceUuid.hpp"

namespace LnxImgBack
{
	/**
	 * @brief Class to represent a mount point
	 * @note This class has some limitations about generating a UUID. See the constructor documentation for more details.
	 */
	class mount_point
	{
		private:

			std::filesystem::path path;				// Mount point path
			std::filesystem::path device_path;		// Device path
			std::string type;						// Filesystem type
			std::vector<std::string> options;		// Mount point options
			bool dump;								// Dump option
			bool pass;								// Pass option

			DeviceUuid uuid;						// Device UUID

		public:

			/**
			 * @brief Create an empty mount point object
			 */
			mount_point ();

			/**
			 * @brief Create an mount point object
			 * @param mountPoint Mount point path
			 * @param diskUuidPath Disk path UUID. Located in /dev/disk/by-uuid.
			 * @param type Filesystem type used by the mount point
			 * @param options Mount point options
			 * @param dump Define as a dump option
			 * @param pass Define as pass option
			 * @note diskUuidPath can be used with other disk paths, like by-label orr by-path. But will not generate the DeviceUuid.
			 */
			mount_point (std::filesystem::path mountPoint, std::filesystem::path diskUuidPath, std::string type, std::vector<std::string> options, bool dump, bool pass);
			
			mount_point (const LnxImgBack::mount_point& other);
			mount_point (LnxImgBack::mount_point&& other) noexcept;

			~mount_point();

			LnxImgBack::mount_point& operator= (const LnxImgBack::mount_point& other);
			LnxImgBack::mount_point& operator= (LnxImgBack::mount_point&& other) noexcept;

			/**
			 * @brief Return the mount point path.
			 * @note If the mount point was empty, will return an empty path
			 */
			std::filesystem::path getMountPoint();

			/**
			 * @brief Return the disk UUID path used to identify this mount point
			 */
			std::filesystem::path getDiskPath();

			/**
			 * @brief Return the mount point options used to configure
			 */
			std::vector<std::string> getOptions();

			/**
			 * @brief Return if the mount point is marked as dump
			 */
			bool isDump();

			/**
			 * @brief Return if the mount point is marked as pass
			 */
			bool isPass();

			/**
			 * @brief Return the device UUID used to this mount point
			 * @note The DeviceUuid is only generated when the object is created using a valid disk path to /dev/disk/by-uuid. Otherwise will return an empty UUID.
			 */
			DeviceUuid getDeviceUuid();
	};
}

#endif // !MOUNT_POINT_HPP