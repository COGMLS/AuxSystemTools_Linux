#pragma once

#ifndef IMAGE_DATA_TYPES_HPP
#define IMAGE_DATA_TYPES_HPP

namespace LnxImgBack
{
	/**
	 * @brief Image Block Size
	 * @details The BlockSize is used only for backup operations. Lower values will result in more time to complete the task
	 * @note The 'dd' tool assumes 512k if the block size is not set by the user
	 */
	enum class BlockSize
	{
		bs16k = 16 * 1024,
		bs32k = 32 * 1024,
		bs64k = 64 * 1024,
		bs128k = 128 * 1024,
		bs256k = 256 * 1024,
		bs512k = 512 * 1024,
		bs1m = 1024 * 1024
	};

	/**
	 * @brief Determinate the type of the image
	 * @details This controls the type of tool is going to be used during the process of Backup/Restore the image
	 */
	enum class ImageType
	{
		StandardImage,
		TarImageType,
		GzipCompressedImage
	};

	/**
	 * @brief Determinate the type of operation is going to be
	 */
	enum class OperationType
	{
		LocalImageBackup,
		LocalImageRestore,
		RemoteImageBackup,
		RemoteImageRestore
	};
}

#endif // !IMAGE_DATA_TYPES_HPP