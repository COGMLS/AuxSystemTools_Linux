#include "Devices.hpp"

LnxImgBack::storage_device::storage_device(std::filesystem::path device_fs_path)
{
	this->device_fs_path = device_fs_path;

	this->size = 0;
	this->attach_status = false;
	this->removable_status = false;
	this->hidden_status = false;
	this->device_state = false;
	this->objStatus = 0;

	this->uuid.push_back(DeviceUuid());

	if (std::filesystem::exists(this->device_fs_path))
	{
		// If a block file was passed, try to find the block folder:
		if (std::filesystem::is_block_file(this->device_fs_path))
		{
			std::string device_block_name = device_fs_path.stem().string();
			this->device_fs_path = std::filesystem::path(SYS_BLOCK_PATH) / device_block_name;

			// Throw an exception for an possible incompatible device with this class:
			if (!std::filesystem::exists(this->device_fs_path))
			{
				LnxImgBack::storage_device_err e(10, STORAGE_DEVICE_ERROR_DEV_FS_PATH_INCOMPATIBLE);
				throw e;
			}
		}

		// If the device_fs_path is not a directory/symlink that leads to a directory or a block device, throw an exception:
		if (
				!std::filesystem::is_directory(this->device_fs_path) || 
				(
					std::filesystem::is_symlink(this->device_fs_path) && 
					!(
						std::filesystem::is_directory(std::filesystem::read_symlink(this->device_fs_path)) || 
						std::filesystem::is_block_file(std::filesystem::read_symlink(this->device_fs_path))
					)
				)
			)
		{
			LnxImgBack::storage_device_err e(10, STORAGE_DEVICE_ERROR_DEV_FS_PATH_INCOMPATIBLE);
			throw e;
		}

		/** Array to store paths to files, links and block files
		 * Device Paths:
		 * 0: device (link)
		 * 1: dev
		 * 2: ext_range
		 * 3: hidden
		 * 4: removable
		 * 5: size
		 * 6: uevent
		 */
		std::array<std::filesystem::path, 7> device_files;

		for (const std::filesystem::directory_entry& d : std::filesystem::directory_iterator(this->device_fs_path))
		{
			if (d.path().stem().string() == "device")
			{
				device_files[0] = d.path();
			}

			if (d.path().stem().string() == "dev")
			{
				device_files[1] = d.path();
			}

			if (d.path().stem().string() == "ext_range")
			{
				device_files[2] = d.path();
			}

			if (d.path().stem().string() == "hidden")
			{
				device_files[3] = d.path();
			}

			if (d.path().stem().string() == "removable")
			{
				device_files[4] = d.path();
			}

			if (d.path().stem().string() == "size")
			{
				device_files[5] = d.path();
			}

			if (d.path().stem().string() == "uevent")
			{
				device_files[6] = d.path();
			}
		}

		unsigned long long ull_ext_range = 0;
		unsigned long long ull_size = 0;
		bool ignorePerms = true;
		
		for (size_t i = 0; i < device_files.size(); i++)
		{
			if (!device_files[i].empty())
			{
				switch (i)
				{
					case 0:
					{
						for (const std::filesystem::directory_entry& d: std::filesystem::directory_iterator(device_files[i]))
						{
							// Get the model name:
							if (d.is_regular_file() && d.path().stem().string() == "model")
							{
								std::vector<std::string> data;
								int extractStatus = extractFile(d.path(), data, ignorePerms);
								if (extractStatus == 0)
								{
									this->device_model = data[0];
								}
							}

							// Get the device status (running or not):
							if (d.is_regular_file() && d.path().stem().string() == "state")
							{
								std::vector<std::string> data;
								int extractStatus = extractFile(d.path(), data, ignorePerms);
								if (extractStatus == 0)
								{
									if (data[0] == "running")
									{
										this->device_state = true;
									}
									else
									{
										this->device_state = false;
									}
								}
							}
						}
						break;
					}
					// Extract the device path:
					case 1:
					{
						if (std::filesystem::exists(device_files[i]))
						{
							if (std::filesystem::is_regular_file(device_files[i]))
							{
								// Extract the file content:
								std::vector<std::string> data;
								int extractStatus = extractFile(device_files[i], data, ignorePerms);
								if (extractStatus == 0)
								{
									if (!data.empty())
									{
										this->device_path = data[0];
									}
								}
							}
						}
						break;
					}
					// Extract the ext_range value:
					case 2:
					{
						if (std::filesystem::exists(device_files[i]))
						{
							if (std::filesystem::is_regular_file(device_files[i]))
							{
								// Extract the file content:
								std::vector<std::string> data;
								int extractStatus = extractFile(device_files[i], data, ignorePerms);
								if (extractStatus == 0)
								{
									if (!data.empty())
									{
										try
										{
											ull_ext_range = std::stoull(data[0]);
										}
										catch(const std::exception&)
										{
											ull_ext_range = 0;
											this->objStatus += 4;
										}
									}
								}
							}
						}
						break;
					}
					// Extract the hidden information:
					case 3:
					{
						if (std::filesystem::exists(device_files[i]))
						{
							if (std::filesystem::is_regular_file(device_files[i]))
							{
								// Extract the file content:
								std::vector<std::string> data;
								int extractStatus = extractFile(device_files[i], data, ignorePerms);
								if (extractStatus == 0)
								{
									if (!data.empty())
									{
										if (data[0] == "1")
										{
											this->hidden_status = true;
										}
										else
										{
											this->hidden_status = false;
										}
									}
								}
							}
						}
						break;
					}
					// Extract if the device is removable:
					case 4:
					{
						if (std::filesystem::exists(device_files[i]))
						{
							if (std::filesystem::is_regular_file(device_files[i]))
							{
								// Extract the file content:
								std::vector<std::string> data;
								int extractStatus = extractFile(device_files[i], data, ignorePerms);
								if (extractStatus == 0)
								{
									if (!data.empty())
									{
										if (data[0] == "1")
										{
											this->removable_status = true;
										}
										else
										{
											this->removable_status = false;
										}
									}
								}
							}
						}
						break;
					}
					// Extract the size value:
					case 5:
					{
						if (std::filesystem::exists(device_files[i]))
						{
							if (std::filesystem::is_regular_file(device_files[i]))
							{
								// Extract the file content:
								std::vector<std::string> data;
								int extractStatus = extractFile(device_files[i], data, ignorePerms);
								if (extractStatus == 0)
								{
									if (!data.empty())
									{
										try
										{
											ull_size = std::stoull(data[0]);
										}
										catch(const std::exception&)
										{
											ull_size = 0;
											this->objStatus += 2;
										}
									}
								}
							}
						}
						break;
					}
					// Extract the uevent information:
					case 6:
					{
						if (std::filesystem::exists(device_files[i]))
						{
							if (std::filesystem::is_regular_file(device_files[i]))
							{
								// Extract the file content:
								std::vector<std::string> data;
								int extractStatus = extractFile(device_files[i], data, ignorePerms);
								if (extractStatus == 0)
								{
									if (!extractFileValue(data, "DEVNAME", this->device))
									{
										this->objStatus += 1;
									}
								}
							}
						}
						break;
					}
					default:
					{
						break;
					}
				}
			}
		}

		// Calculate the device capacity in bytes:
		if (ull_ext_range != 0 && ull_size != 0)
		{
			this->size = ull_size * 2 * ull_ext_range;
		}
		else
		{
			this->size = 0;
		}

		// Get the associated UUIDs with the storage device:
		for (const std::filesystem::directory_entry& d : std::filesystem::directory_iterator("/dev/disk/by-uuid"))
		{
			DeviceUuid uuid(d);

			if (!uuid.device().empty())
			{
				if (uuid.device().starts_with(this->device))
				{
					this->uuid.push_back(uuid);
				}
			}
		}

		// Organize the founded UUID devices with the storage uuid vector index (Index 0 is reserved to the current device storage):
		if (!this->uuid.empty())
		{
			for (int i = 1; i < this->uuid.size() - 1; i++)
			{
				int j = i + 1;
				for (j; j < this->uuid.size(); j++)
				{
					if (this->uuid[i].index() > this->uuid[j].index())
					{
						std::swap<DeviceUuid>(this->uuid[i], this->uuid[j]);
					}
				}
			}
		}
	}
}

LnxImgBack::storage_device::storage_device(std::string device_name)
{
	std::filesystem::path device_fs_path = std::filesystem::path(SYS_BLOCK_PATH) / device_name;
	LnxImgBack::storage_device other(device_fs_path);
	*this = other;
}

LnxImgBack::storage_device::storage_device(const char device_name[])
{
	std::filesystem::path device_fs_path = std::filesystem::path(SYS_BLOCK_PATH) / device_name;
	LnxImgBack::storage_device other(device_fs_path);
	*this = other;
}

LnxImgBack::storage_device::storage_device(const storage_device &other)
{
	this->uuid = other.uuid;
	this->device_fs_path = other.device_fs_path;
	this->device = other.device;
	this->device_path = other.device_path;
	this->device_model = other.device_model;
	this->size = other.size;
	this->attach_status = other.attach_status;
	this->removable_status = other.removable_status;
	this->hidden_status = other.hidden_status;
	this->device_state = other.device_state;
	this->objStatus = other.objStatus;
}

LnxImgBack::storage_device::storage_device(storage_device &&other) noexcept
{
	this->uuid = std::move(other.uuid);
	this->device_fs_path = std::move(other.device_fs_path);
	this->device = std::move(other.device);
	this->device_path = std::move(other.device_path);
	this->device_model = std::move(other.device_model);
	this->size = std::move(other.size);
	this->attach_status = std::move(other.attach_status);
	this->removable_status = std::move(other.removable_status);
	this->hidden_status = std::move(other.hidden_status);
	this->device_state = std::move(other.device_state);
	this->objStatus = std::move(other.objStatus);
}

LnxImgBack::storage_device::~storage_device()
{
}

LnxImgBack::storage_device &LnxImgBack::storage_device::operator=(const LnxImgBack::storage_device &other)
{
    this->uuid = other.uuid;
	this->device_fs_path = other.device_fs_path;
	this->device = other.device;
	this->device_path = other.device_path;
	this->device_model = other.device_model;
	this->size = other.size;
	this->attach_status = other.attach_status;
	this->removable_status = other.removable_status;
	this->hidden_status = other.hidden_status;
	this->device_state = other.device_state;
	this->objStatus = other.objStatus;

	return *this;
}

LnxImgBack::storage_device &LnxImgBack::storage_device::operator=(LnxImgBack::storage_device &&other) noexcept
{
    if (this == &other)
	{
		return *this;
	}

	this->uuid = std::move(other.uuid);
	this->device_fs_path = std::move(other.device_fs_path);
	this->device = std::move(other.device);
	this->device_path = std::move(other.device_path);
	this->device_model = std::move(other.device_model);
	this->size = std::move(other.size);
	this->attach_status = std::move(other.attach_status);
	this->removable_status = std::move(other.removable_status);
	this->hidden_status = std::move(other.hidden_status);
	this->device_state = std::move(other.device_state);
	this->objStatus = std::move(other.objStatus);
	
	return *this;
}

void LnxImgBack::storage_device::refresh()
{
	LnxImgBack::storage_device other(this->device_fs_path);
	*this = other;
}

DeviceUuid LnxImgBack::storage_device::getUuid()
{
    return this->uuid[0];
}

std::string LnxImgBack::storage_device::getDevice()
{
    return this->device;
}

unsigned long long LnxImgBack::storage_device::getSize()
{
    return this->size;
}

bool LnxImgBack::storage_device::isInUse()
{
    return this->attach_status;
}

std::string LnxImgBack::storage_device::getDevPath()
{
    return this->device_path;
}

std::string LnxImgBack::storage_device::getModel()
{
    return this->device_model;
}

std::filesystem::path LnxImgBack::storage_device::getPath()
{
    return this->device_fs_path;
}

std::vector<DeviceUuid> LnxImgBack::storage_device::getAssociatedUuid()
{
    return this->uuid;
}
