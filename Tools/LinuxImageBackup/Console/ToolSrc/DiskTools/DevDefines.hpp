#pragma once

#ifndef IMAGE_TOOL_DEVICES_DEFINITIONS_HPP
#define IMAGE_TOOL_DEVICES_DEFINITIONS_HPP

#define SYS_BLOCK_PATH 		"/sys/block"
#define FSTAB_FILE_PATH 	"/etc/fstab"
#define DISK_UUID_PATH		"/dev/disk/by-uuid"

#define SYS_BLOCK_DEVICE_SIZE_FILE "size"
#define SYS_BLOCK_DEVICE_BLOCKSIZE "ext_range"

#define DEVICE_IDE_TYPE 	"hd"
#define DEVICE_SCSI_TYPE 	"sd"
#define DEVICE_NVME_TYPE 	"nvme"
#define DEVICE_MMC_TYPE 	"mmcblk"

#endif // !IMAGE_TOOL_DEVICES_DEFINITIONS_HPP