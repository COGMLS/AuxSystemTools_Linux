#include "ErrorClasses.hpp"

LnxImgBack::storage_device_err::storage_device_err(int code, const char category[])
{
	this->code = code;
	this->category = category;
}

LnxImgBack::storage_device_err::storage_device_err(const LnxImgBack::storage_device_err &other)
{
	this->code = other.code;
	this->category = other.category;
}

LnxImgBack::storage_device_err::~storage_device_err()
{
}

const char *LnxImgBack::storage_device_err::what() const noexcept
{
	std::string errMsg = this->category + " | Code: " + std::to_string(this->code);
    char* errMsgC = new char[errMsg.size()];
	std::strcpy(errMsgC, errMsg.c_str());
	return const_cast<const char*>(errMsgC);
}

LnxImgBack::storage_device_err &LnxImgBack::storage_device_err::operator=(const LnxImgBack::storage_device_err &other) noexcept
{
	this->code = other.code;
	this->category = other.code;
	return *this;
}
