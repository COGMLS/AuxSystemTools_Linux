#pragma once

#ifndef FILE_TOOLS_HPP
#define FILE_TOOLS_HPP

#include <fstream>
#include <string>
#include <vector>
#include <filesystem>

int extractFile (std::filesystem::path filepath, std::vector<std::string>& data);

int writeFile (std::filesystem::path filepath, std::vector<std::string>& data, char writingType);

bool extractFileValue (std::vector<std::string>& data, std::string key, std::string& value);

bool extractFileValue (std::vector<std::string>& data, std::string key, long long& value);

bool extractFileValue (std::vector<std::string>& data, std::string key, unsigned long long value);

#endif // !FILE_TOOLS_HPP