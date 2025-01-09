#pragma once

#ifndef IMAGE_TOOL_DEVICES_HPP
#define IMAGE_TOOL_DEVICES_HPP

#include <string>
#include <cstring>
#include <vector>
#include <fstream>
#include <array>

#include "DeviceUuid.hpp"
#include "DevDefines.hpp"

#include "../Common/FileTools.hpp"
#include "../Common/ToolExceptions.hpp"

namespace LnxImgBack
{
	/**
	 * @brief Class to hold information about storage devices
	 */
	class storage_device
	{
		private:

			// Store the UUIDs associated with the storage device:
			// Index 0: Device (Can be empty if was not recovered)
			// Other indexes: device partitions (using the same index by the system. i.e. sdb1, sdb2)
			std::vector<DeviceUuid> uuid;

			// Device FS path:
			std::filesystem::path device_fs_path;

			// Device name. I.e. sda, hda, etc.
			std::string device;

			// Device path:
			std::string device_path;

			// Device Model:
			std::string device_model;

			// Storage Capacity (in bytes) [NOTE: Zero means the value was not possible to determinate]:
			unsigned long long size;

			// Device status (false - detached, true - attached):
			bool attach_status;

			// Device is removable:
			bool removable_status;

			// Device is hidden:
			bool hidden_status;

			// Device is running:
			bool device_state;

			// Object Status: Controls if the object is ready for use
			unsigned int objStatus;

		public:

			/**
			 * @brief Create an storage device object to represent the system storage (sda, hda, etc)
			 * @param device_fs_path Path to device block, located in /sys/block
			 */
			storage_device (std::filesystem::path device_fs_path);

			/**
			 * @brief Create an storage device object to represent the system storage (sda, hda, etc)
			 * @param device_name Device name. Like sda, sdb, etc.
			 */
			storage_device (std::string device_name);

			/**
			 * @brief Create an storage device object to represent the system storage (sda, hda, etc)
			 * @param device_name Device name. Like sda, sdb, etc.
			 */
			storage_device (const char device_name[]);

			storage_device (const storage_device& other);

			storage_device (storage_device&& other) noexcept;

			~storage_device();

			//bool operator== (const LnxImgBack::storage_device& other);

			//bool operator== (const LnxImgBack::storage_device& other);

			LnxImgBack::storage_device& operator= (const LnxImgBack::storage_device& other);

			LnxImgBack::storage_device& operator= (LnxImgBack::storage_device&& other) noexcept;

			void refresh();

			DeviceUuid getUuid();

			std::string getDevice();

			unsigned long long getSize();

			bool isInUse();

			std::string getDevPath();

			std::string getModel();

			std::filesystem::path getPath();

			std::vector<DeviceUuid> getAssociatedUuid();
	};
}

#endif // !IMAGE_TOOL_DEVICES_HPP