#include "MountPoint.hpp"

LnxImgBack::mount_point::mount_point()
{
	this->dump = false;
	this->pass = false;
}

LnxImgBack::mount_point::mount_point(std::filesystem::path mountPoint, std::filesystem::path diskUuidPath, std::string type, std::vector<std::string> options, bool dump, bool pass)
{
	this->path = mountPoint;
	this->device_path = diskUuidPath;
	this->type = type;
	this->options = options;
	this->dump = dump;
	this->pass = pass;

	if (this->device_path.string().starts_with(DISK_UUID_PATH))
	{
		this->uuid = DeviceUuid(this->device_path);
	}
}

LnxImgBack::mount_point::mount_point(const LnxImgBack::mount_point &other)
{
	this->path = other.path;
	this->device_path = other.device_path;
	this->type = other.type;
	this->options = other.options;
	this->dump = other.dump;
	this->pass = other.pass;
	this->uuid = other.uuid;
}

LnxImgBack::mount_point::mount_point(LnxImgBack::mount_point &&other) noexcept
{
	this->path = std::move(other.path);
	this->device_path = std::move(other.device_path);
	this->type = std::move(other.type);
	this->options = std::move(other.options);
	this->dump = std::move(other.dump);
	this->pass = std::move(other.pass);
	this->uuid = std::move(other.uuid);
}

LnxImgBack::mount_point::~mount_point()
{
}

LnxImgBack::mount_point &LnxImgBack::mount_point::operator=(const LnxImgBack::mount_point &other)
{
    this->path = other.path;
	this->device_path = other.device_path;
	this->type = other.type;
	this->options = other.options;
	this->dump = other.dump;
	this->pass = other.pass;
	this->uuid = other.uuid;
	return *this;
}

LnxImgBack::mount_point &LnxImgBack::mount_point::operator=(LnxImgBack::mount_point &&other) noexcept
{
    if (this == &other)
	{
		return *this;
	}

	this->path = std::move(other.path);
	this->device_path = std::move(other.device_path);
	this->type = std::move(other.type);
	this->options = std::move(other.options);
	this->dump = std::move(other.dump);
	this->pass = std::move(other.pass);
	this->uuid = std::move(other.uuid);

	return *this;
}

std::filesystem::path LnxImgBack::mount_point::getMountPoint()
{
    return this->path;
}

std::filesystem::path LnxImgBack::mount_point::getDiskPath()
{
    return this->device_path;
}

std::vector<std::string> LnxImgBack::mount_point::getOptions()
{
    return this->options;
}

bool LnxImgBack::mount_point::isDump()
{
    return this->dump;
}

bool LnxImgBack::mount_point::isPass()
{
    return this->pass;
}

DeviceUuid LnxImgBack::mount_point::getDeviceUuid()
{
    return this->uuid;
}
