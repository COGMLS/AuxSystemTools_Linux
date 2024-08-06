#pragma once

#ifndef FONT_PACK_HPP
#define FONT_PACK_HPP

#include "pch.h"
#include "listPack.hpp"

#include <string>
#include <vector>
#include <filesystem>
#include <exception>
#include <stdexcept>
#include <algorithm>

class fontPack
{
    private:
        std::filesystem::path packPath;
        std::wstring packName;
        installType type;
        bool isInstalled;

    public:

        /**
         * @brief Create an font pack, detecting if is a user or system installation.
         * @param fontPackDir Font pack directory's path.
         */
        fontPack (std::filesystem::path fontPackDir);

        /**
         * @brief Create an font pack object that can represent a installed pack or a font pack that needs to be install.
         * @param fontPackDir Font pack directory's path.
         * @param sysInstall Force to determinate if will be a system install.
         */
        fontPack (std::filesystem::path fontPackDir, bool sysInstall);

        ~fontPack();

        /**
         * @brief Install the font pack
         * @return -1 if fail to install.
         * @return 0 if no changes was made in the system.
         * @return 1 if the font pack was installed.
         */
        int install();

        /**
         * @brief Remove the font pack
         * @return -1 if fail to remove.
         * @return 0 if no changes was made in the system.
         * @return 1 if the font pack was remove.
         */
        int remove();

        /**
         * @brief Export a list of properties about the font pack
         */
        listPack getPackInfo();
};

#endif // !FONT_PACK_HPP