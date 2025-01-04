#pragma once

#ifndef DEVICE_UUID_HPP
#define DEVICE_UUID_HPP

#include <string>
#include <cstring>
#include <cctype>
#include <vector>
#include <filesystem>

/**
 * @brief Detect and holds a Device UUID
 * @note This class does not check if the UUID is valid or not. Only holds the given data and process the segments into a vector, removing the dashes.
 */
class DeviceUuid
{
	private:

		std::vector<std::string> uuid;
		std::string device_name;

	public:

		/**
		 * @brief Create an empty Device UUID object.
		 * @note This object will return empty strings for UUID and Device Name.
		 */
		DeviceUuid();

		/**
		 * @brief Store a Device UUID based on given string
		 * @param uuid_str UUID string
		 */
		DeviceUuid (std::string uuid_str);
		
		/**
		 * @brief Search for a block device and holds the UUID and the reference to the device
		 * @param uuid_device_path Path to a device block. I.e. /dev/disk/by-uuid/sda1
		 */
		DeviceUuid (std::filesystem::path uuid_device_path);

		DeviceUuid (const DeviceUuid& other);

		DeviceUuid (DeviceUuid&& other) noexcept;

		~DeviceUuid();

		/**
		 * @brief Transform the UUID segments stored in the vector as a string value
		 * @param noDashes If true, no dashes will be added
		 * @return Return a UUID string value
		 * @note The UUID string characters are converted to lowercase.
		 */
		std::string to_string (bool noDashes = false);

		/**
		 * @brief Get the device associated with the UUID, if the object was created with a valid block device path
		 * @return If valid a string with the name to the device will return
		 */
		std::string device();

		bool operator== (const DeviceUuid& other);

		bool operator!= (const DeviceUuid& other);

		bool operator== (const std::string& uuid_str);

		DeviceUuid& operator= (const DeviceUuid& other);

		DeviceUuid& operator= (DeviceUuid&& other) noexcept;
};

std::string uuidArr2Str (std::vector<std::string> uuid, bool noDashes);

void uuidStr2lower (std::string& str);

#endif // !DEVICE_UUID_HPP