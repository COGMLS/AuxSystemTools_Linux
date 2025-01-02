#include "TypesTools.hpp"

std::string LnxImgBack::convertBlockSize(LnxImgBack::BlockSize bs)
{
	switch (bs)
	{
		case LnxImgBack::BlockSize::bs16k:
		{
			return "16k";
		}
		case LnxImgBack::BlockSize::bs32k:
		{
			return "32k";
		}
		case LnxImgBack::BlockSize::bs64k:
		{
			return "64k";
		}
		case LnxImgBack::BlockSize::bs128k:
		{
			return "128k";
		}
		case LnxImgBack::BlockSize::bs256k:
		{
			return "265k";
		}
		case LnxImgBack::BlockSize::bs512k:
		{
			return "512k";
		}
		case LnxImgBack::BlockSize::bs1m:
		{
			return "1m";
		}
		default:
		{
			return "512k";
		}
	}
}