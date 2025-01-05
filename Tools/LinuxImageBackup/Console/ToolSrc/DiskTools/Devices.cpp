#include "Devices.hpp"

LnxImgBack::storage_device::storage_device(std::filesystem::path device_path)
{
	this->uuid.push_back(DeviceUuid());

	if (std::filesystem::exists(device_path))
	{
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

		for (const std::filesystem::directory_entry& d : std::filesystem::directory_iterator(device_path))
		{
			if (d.path().stem() == "device")
			{
				device_files[0] = d.path();
			}

			if (d.path().stem() == "dev")
			{
				device_files[1] = d.path();
			}

			if (d.path().stem() == "ext_range")
			{
				device_files[2] = d.path();
			}

			if (d.path().stem() == "hidden")
			{
				device_files[3] = d.path();
			}

			if (d.path().stem() == "removable")
			{
				device_files[4] = d.path();
			}

			if (d.path().stem() == "size")
			{
				device_files[5] = d.path();
			}

			if (d.path().stem() == "uevent")
			{
				device_files[6] = d.path();
			}
		}

		unsigned long long ull_ext_range = 0;
		unsigned long long ull_size = 0;
		
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
								if (extractFile(d.path(), data) == 0)
								{
									this->device_model = data[0];
								}
							}

							// Get the device status (running or not):
							if (d.is_regular_file() && d.path().stem().string() == "state")
							{
								std::vector<std::string> data;
								if (extractFile(d.path(), data) == 0)
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
								if (extractFile(device_files[i], data) == 0)
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
								if (extractFile(device_files[i], data) == 0)
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
								if (extractFile(device_files[i], data) == 0)
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
								if (extractFile(device_files[i], data) == 0)
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
								if (extractFile(device_files[i], data) == 0)
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
								if (extractFile(device_files[i], data) == 0)
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
		if (!this->device.empty())
		{
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
		}
	}
}