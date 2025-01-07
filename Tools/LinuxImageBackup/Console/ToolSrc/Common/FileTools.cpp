#include "FileTools.hpp"

int extractFile(std::filesystem::path filepath, std::vector<std::string> &data, bool ignoreFilePerms)
{
	if (!std::filesystem::exists(filepath))
	{
		return 1;
	}

	if (!std::filesystem::is_regular_file(filepath))
	{
		return 2;
	}

	std::vector<std::string> _data;

	std::fstream fs;

	std::filesystem::file_status status = std::filesystem::status(filepath);

	if ((status.permissions() & std::filesystem::perms::owner_read) == std::filesystem::perms::owner_read && !ignoreFilePerms)
	{
		return 5;
	}

	fs.open(filepath, std::ios_base::in);

	if (!fs.is_open())
	{
		return 3;
	}

	try
	{
		std::string tmp;
		while (std::getline(fs, tmp))
		{
			_data.push_back(tmp);
			tmp.clear();
		}
		fs.close();
	}
	catch(const std::exception&)
	{
		return 4;
	}

	data = _data;

    return 0;
}

int writeFile(std::filesystem::path filepath, std::vector<std::string> &data, short writingType, bool ignoreFilePerms)
{
	bool file_exist = std::filesystem::exists(filepath);

	// If the file does not exist, check if the parent exist to create it
    if (!file_exist)
	{
		if (!std::filesystem::exists(filepath.parent_path()))
		{
			return 1;
		}
	}

	if (!std::filesystem::is_regular_file(filepath))
	{
		return 2;
	}

	std::vector<std::string> _data;

	std::fstream fs;

	if (file_exist)
	{
		std::filesystem::file_status status = std::filesystem::status(filepath);

		if (
				(status.permissions() & std::filesystem::perms::owner_read) == std::filesystem::perms::owner_read && 
				(status.permissions() & std::filesystem::perms::owner_write) == std::filesystem::perms::owner_write && 
				!ignoreFilePerms
			)
		{
			return 5;
		}

		if (writingType > 2)
		{
			return 6;
		}

		if (writingType == 0)
		{
			fs.open(filepath, std::ios_base::out | std::ios_base::trunc);
		}
		
		if (writingType == 1)
		{
			int extraction = extractFile(filepath, _data);
			if (extraction != 0)
			{
				return extraction;
			}
			fs.open(filepath, std::ios_base::out);
		}

		if (writingType == 2)
		{
			fs.open(filepath, std::ios_base::out | std::ios_base::ate);
		}
	}
	else
	{
		std::filesystem::file_status status = std::filesystem::status(filepath);

		if (
				(status.permissions() & std::filesystem::perms::owner_read) == std::filesystem::perms::owner_read && 
				(status.permissions() & std::filesystem::perms::owner_write) == std::filesystem::perms::owner_write && 
				!ignoreFilePerms
			)
		{
			return 5;
		}

		fs.open(filepath, std::ios_base::out);
	}

	if (!fs.is_open())
	{
		return 3;
	}

	try
	{
		for (size_t i = 0; i < data.size(); i++)
		{
			fs << data[i] << std::endl;
		}

		if (writingType == 1)
		{
			for (size_t i = 0; i < _data.size(); i++)
			{
				fs << _data[i] << std::endl;
			}
		}

		fs.close();
	}
	catch(const std::exception&)
	{
		fs.close();
		return 4;
	}

    return 0;
}

bool extractFileValue(std::vector<std::string> &data, std::string key, std::string &value)
{
	key += "=";

	for (size_t i = 0; i < data.size(); i++)
	{
		if (data[i].starts_with(key))
		{
			value = data[i].substr(key.size(), data[i].size() - key.size());
			return true;
		}
	}

    return false;
}

bool extractFileValue(std::vector<std::string> &data, std::string key, long long &value)
{
	std::string tmp;

	if (extractFileValue(data, key, tmp))
	{
		try
		{
			long long ll = std::stoll(tmp);
			value = ll;
			return true;
		}
		catch(const std::exception&)
		{
			return false;
		}
	}

    return false;
}

bool extractFileValue(std::vector<std::string> &data, std::string key, unsigned long long value)
{
	std::string tmp;

	if (extractFileValue(data, key, tmp))
	{
		try
		{
			unsigned long long ull = std::stoull(tmp);
			value = ull;
			return true;
		}
		catch(const std::exception&)
		{
			return false;
		}
	}

    return false;
}
