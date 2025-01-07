#pragma once

#ifndef FILE_TOOLS_HPP
#define FILE_TOOLS_HPP

#include <fstream>
#include <string>
#include <vector>
#include <filesystem>

/**
 * @brief Extract the file lines into a vector of strings
 * @param filepath File path
 * @param data Vector to hold the file lines
 * @return 0 if success extract the file lines
 * @return 1 if the filepath does not exist
 * @return 2 if is not a regular file
 * @return 3 if was not possible to open the file
 * @return 4 if an exception occur
 * @return 5 if the user does not have permission to reade/write the file
 */
int extractFile (std::filesystem::path filepath, std::vector<std::string>& data);

/**
 * @brief Write the vector of strings into a file
 * @param filepath File path
 * @param data Vector that holds the files lines
 * @param writingType 0: Rewrite the complete file (lost previous data). 1: Insert the new data on begin of the file. 2: Insert the new data on the end of the file. Any other value will make the function return 6 (Invalid argument).
 * @return 0 successful wrote the file lines
 * @return 1 if the filepath does not exist
 * @return 2 if is not a regular file
 * @return 3 if was not possible to open the file
 * @return 4 if an exception occur
 * @return 5 if the user does not have permission to reade/write the file
 * @return 6 if an invalid argument was passed
 */
int writeFile (std::filesystem::path filepath, std::vector<std::string>& data, short writingType = 2);

/**
 * @brief Extract a value inside a file with key-pair data: <key>=<value>.
 * @param data Vector that holds the file lines
 * @param key Key value. Do not use the assign character '='
 * @param value Reference variable to receive the extracted value
 * @return TRUE if the data was successfully extracted.
 * @return FALSE if the data was not found.
 * @note The extracted data is in raw text format, if is a numeric value, use the other functions to try to convert during the extraction task.
 */
bool extractFileValue (std::vector<std::string>& data, std::string key, std::string& value);

/**
 * @brief Extract a value inside a file with key-pair data: <key>=<value>.
 * @param data Vector that holds the file lines
 * @param key Key value. Do not use the assign character '='
 * @param value Reference variable to receive the extracted value
 * @return TRUE if the data was successfully extracted.
 * @return FALSE if the data was not found or is incompatible with the value.
 */
bool extractFileValue (std::vector<std::string>& data, std::string key, long long& value);

/**
 * @brief Extract a value inside a file with key-pair data: <key>=<value>.
 * @param data Vector that holds the file lines
 * @param key Key value. Do not use the assign character '='
 * @param value Reference variable to receive the extracted value
 * @return TRUE if the data was successfully extracted.
 * @return FALSE if the data was not found or is incompatible with the value.
 */
bool extractFileValue (std::vector<std::string>& data, std::string key, unsigned long long value);

#endif // !FILE_TOOLS_HPP