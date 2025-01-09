#include "DeviceUuid.hpp"

std::string uuidArr2Str(std::vector<std::string> uuid, bool noDashes)
{
    std::string uuid_str;

	for (size_t i = 0; i < uuid.size(); i++)
	{
		if (!noDashes)
		{
			if (i + 1 < uuid.size())
			{
				uuid_str += uuid[i] + "-";
			}
			else
			{
				uuid_str += uuid[i];
			}
		}
		else
		{
			uuid_str += uuid[i];
		}
	}

	return uuid_str;
}

void uuidStr2lower(std::string &str)
{
	for (size_t i = 0; i < str.size(); i++)
	{
		if (std::isupper(str[i]))
		{
			str[i] = std::tolower(str[i]);
		}
	}
}

DeviceUuid::DeviceUuid()
{
	this->device_index = -1;	
}

DeviceUuid::DeviceUuid(std::string uuid_str)
{
	this->device_index = -1;
	
	uuidStr2lower(uuid_str);

	char* c_uuid_str = const_cast<char*>(uuid_str.c_str());
	const char* delim = "-";
	char* token = std::strtok(c_uuid_str, delim);

	while (token)
	{
		if (token != nullptr)
		{
			this->uuid.push_back(token);
		}
		token = std::strtok(nullptr, delim);
	}
}

DeviceUuid::DeviceUuid(std::filesystem::path uuid_device_path)
{
	if (std::filesystem::is_block_file(uuid_device_path))
	{
		// Get the device name from uuid symlink path:
		std::filesystem::path device_path = std::filesystem::read_symlink(uuid_device_path);
		this->device_name = device_path.stem().string();

		// try to extract the device index, if exists:
		long index_start = -1;
		long index_end = this->device_name.size() - 1;
		std::string indexStr = "";

		for (long i = this->device_name.size() - 1; i >= 0; i--)
		{
			if (this->device_name[i] >= '0' && this->device_name[i] <= '9')
			{
				index_start = i;
			}
		}

		if (index_start > 0)
		{
			indexStr = this->device_name.substr(index_start, (index_end - index_start + 1));
			try
			{
				this->device_index = std::stoi(indexStr);
			}
			catch(const std::exception&)
			{
				this->device_index = -1;
			}
		}

		std::string uuid_str = uuid_device_path.stem().string();

		uuidStr2lower(uuid_str);

		char* c_uuid_str = const_cast<char*>(uuid_str.c_str());
		const char* delim = "-";
		char* token = std::strtok(c_uuid_str, delim);

		while (token)
		{
			if (token != nullptr)
			{
				this->uuid.push_back(token);
			}
			token = std::strtok(nullptr, delim);
		}
	}
}

DeviceUuid::DeviceUuid(const DeviceUuid &other)
{
	this->uuid = other.uuid;
	this->device_name = other.device_name;
	this->device_index = other.device_index;
}

DeviceUuid::DeviceUuid(DeviceUuid &&other) noexcept
{
	this->uuid = std::move(other.uuid);
	this->device_name = std::move(other.device_name);
	this->device_index = std::move(other.device_index);
}

DeviceUuid::~DeviceUuid()
{
}

std::string DeviceUuid::to_string(bool noDashes)
{
	return uuidArr2Str(this->uuid, noDashes);
}

std::string DeviceUuid::device()
{
    return this->device_name;
}

int DeviceUuid::index()
{
    return this->device_index;
}

bool DeviceUuid::operator==(const DeviceUuid &other)
{
    return this->to_string() == uuidArr2Str(other.uuid, false);
}

bool DeviceUuid::operator!=(const DeviceUuid &other)
{
    return !(*this == other);
}

bool DeviceUuid::operator==(const std::string &uuid_str)
{
    bool hasDashes = false;

	for (size_t i = 0; i < uuid_str.size(); i++)
	{
		if (uuid_str[i] == '-')
		{
			hasDashes = true;
			break;
		}
	}

	std::string tmp = uuid_str;

	uuidStr2lower(tmp);

	return this->to_string(!hasDashes) == tmp;
}

DeviceUuid &DeviceUuid::operator=(const DeviceUuid &other)
{
    this->uuid = other.uuid;
	this->device_name = other.device_name;
	this->device_index = other.device_index;
	return *this;
}

DeviceUuid &DeviceUuid::operator=(DeviceUuid &&other) noexcept
{
	if (this == &other)
	{
		return *this;
	}

	this->uuid = std::move(other.uuid);
	this->device_name = std::move(other.device_name);
	this->device_index = std::move(other.device_index);
	return *this;
}
