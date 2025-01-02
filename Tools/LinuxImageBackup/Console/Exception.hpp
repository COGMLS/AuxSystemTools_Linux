#pragma once

#ifndef EXCEPTION_HPP
#define EXCEPTION_HPP

#include <string>
#include <exception>

class CustomException : std::exception
{
	private:

		std::string message;

	public:

		CustomException();

		CustomException(std::string message);

		CustomException(const CustomException& other);

		CustomException(CustomException&& other) noexcept;

		~CustomException();

		const char* what();
};

#endif // !EXCEPTION_HPP