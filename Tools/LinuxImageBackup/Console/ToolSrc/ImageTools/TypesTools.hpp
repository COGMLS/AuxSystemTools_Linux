#pragma once

#ifndef IMAGE_TYPES_TOOLS_HPP
#define IMAGE_TYPES_TOOLS_HPP

#include <string>
#include <cstring>
#include <vector>
#include <cstdlib>

#include "Types.hpp"

namespace LnxImgBack
{
	/**
	 * @brief Convert the BlockSize enum to string to get used in 'dd' tool
	 * @param bs BlockSize value
	 * @return Block size converted value to string
	 */
	std::string convertBlockSize (LnxImgBack::BlockSize bs);
}

#endif // !IMAGE_TYPES_TOOLS_HPP