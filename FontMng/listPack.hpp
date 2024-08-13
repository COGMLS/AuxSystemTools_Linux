#pragma once

#ifndef LIST_PACK_HPP
#define LIST_PACK_HPP

#include "pch.h"
#include "constants.hpp"

#include <vector>
#include <string>
#include <list>
#include <filesystem>

enum installType
{
    USER_INSTALL,
    SYSTEM_INSTALL
};

struct listPack
{
    std::wstring name;
    installType type;
    bool installed;
};

std::list<std::wstring> getFontsList (bool listSysFonts, bool useOnlyNames);

/**
 * @brief Print list of packages to install
 * @param list List of font packs to install
 * @param maxWidth Maximum Width used on console window
 */
void printList(std::vector<listPack> &list, unsigned int maxWidth);

#endif // !LIST_PACK_HPP