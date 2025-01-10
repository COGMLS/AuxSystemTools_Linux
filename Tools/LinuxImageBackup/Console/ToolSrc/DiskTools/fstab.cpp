#include "fstab.hpp"

int LnxImgBack::getAutoMountPoints(std::vector<LnxImgBack::mount_point> &mountPoints)
{
	std::vector<std::array<std::string, 6>> fstab_info = extractFsTabFileInfo();

	if (fstab_info.empty())
	{
		return 1;
	}

	for (size_t i = 0; i < fstab_info.size(); i++)
	{
		bool dump = false;
		bool pass = false;
		std::filesystem::path diskUuidPath = fstab_info[i][0];
		
		std::filesystem::path mountPointPath;
		if (fstab_info[i][1] != "none")
		{
			mountPointPath = fstab_info[i][1];
		}

		std::vector<std::string> options;
		std::string tmp;

		for (size_t j = 0; j < fstab_info[i][3].size(); j++)
		{
			if (fstab_info[i][3][j] == ',')
			{
				options.push_back(tmp);
				tmp.clear();
			}
			else
			{
				tmp += fstab_info[i][3][j];
			}
		}
		
		if (fstab_info[i][4] == "1")
		{
			dump = true;
		}

		if (fstab_info[i][5] == "1")
		{
			pass = true;
		}

		if (std::filesystem::exists(diskUuidPath))
		{
			LnxImgBack::mount_point mp(mountPointPath, diskUuidPath, fstab_info[i][2], options, dump, pass);
			mountPoints.push_back(mp);
		}
	}

    return 0;
}

std::vector<std::array<std::string, 6>> LnxImgBack::extractFsTabFileInfo()
{
    std::vector<std::array<std::string, 6>> fstab_info;

	std::filesystem::path fstabPath = FSTAB_FILE_PATH;

	if (std::filesystem::exists(fstabPath))
	{
		// Extract the fstab file into the memory:
		std::vector<std::string> fstab;

		if (extractFile(fstabPath, fstab, true) != 0)
		{
			return fstab_info;
		}

		// Check line-by-line for comments and data:
		for (size_t i = 0; i < fstab.size(); i++)
		{
			std::vector<std::string> line = extractLineInfo(fstab[i]);

			if (!line.empty())
			{
				if (!line[0].starts_with('#'))
				{
					std::array<std::string, 6> info;

					for (size_t j = 0; j < line.size() && j < 6; j++)
					{
						info[j] = line[j];
					}

					fstab_info.push_back(info);
				}
			}
		}
	}

	return fstab_info;
}

std::vector<std::string> LnxImgBack::extractLineInfo(std::string line)
{
    std::vector<std::string> lineArr;

	size_t i = 0;
	std::string tmp;
	while (i < line.size())
	{
		if (line[i] != ' ' && line[i] != '\t')
		{
			tmp += line[i];
		}

		if (line[i] == ' ' || line[i] == '\t' || i + 1 == line.size())
		{
			lineArr.push_back(tmp);
			tmp.clear();
		}

		i++;
	}

	return lineArr;
}
