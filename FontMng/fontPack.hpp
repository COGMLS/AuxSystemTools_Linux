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

class fontPack
{
    private:
        std::filesystem::path path;
        std::wstring packName;
        installType type;
        bool isInstalled;

    public:
        fontPack(std::filesystem::path fontPackDir);
        ~fontPack();
        void install();
        void remove();
        listPack getPackInfo();
};

#endif // !FONT_PACK_HPP