#pragma once

#ifndef FONT_PACK_HPP
#define FONT_PACK_HPP

#include "pch.h"
#include "listPack.hpp"

#include <string>
#include <vector>
#include <filesystem>

class fontPack
{
    private:
        std::filesystem::path path;
        std::wstring packName;
        installType type;

    public:
        fontPack(std::filesystem::path fontPackDir);
        ~fontPack();
        void install();
        void remove();
        listPack GetPackInfo();
};

#endif // !FONT_PACK_HPP