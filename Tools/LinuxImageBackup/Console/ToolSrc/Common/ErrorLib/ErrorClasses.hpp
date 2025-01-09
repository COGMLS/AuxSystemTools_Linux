#pragma once

#ifndef ERROR_CLASSES_HPP
#define ERROR_CLASSES_HPP

#include <string>
#include <cstring>
#include <exception>

namespace LnxImgBack
{
	class storage_device_err : public std::exception
	{
		private:

			int code;
			std::string category;

		public:

			storage_device_err (int code, const char category[]);

			storage_device_err (const LnxImgBack::storage_device_err& other);

			~storage_device_err();

			const char* what() const noexcept;

			LnxImgBack::storage_device_err& operator= (const LnxImgBack::storage_device_err& other) noexcept;
	};
}


#endif // !ERROR_CLASSES_HPP