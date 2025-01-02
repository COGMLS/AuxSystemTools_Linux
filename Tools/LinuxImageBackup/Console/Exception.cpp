#include "Exception.hpp"

CustomException::CustomException()
{
	
}

CustomException::CustomException(std::string message)
{
	this->message = message;
}

CustomException::CustomException(const CustomException &other)
{
	this->message = other.message;
}

CustomException::CustomException(CustomException &&other) noexcept
{
	this->message = std::move(other.message);
}

CustomException::~CustomException()
{

}

const char *CustomException::what()
{
	return this->message.c_str();
}
