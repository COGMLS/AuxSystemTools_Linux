#include "fontPack.hpp"

fontPack::fontPack(std::filesystem::path fontPackDir)
{
    // Test the path if is a directory:
    if (!std::filesystem::is_directory(fontPackDir))
    {
        std::string msg = "Only a directory package can be used. Path: ";
        msg += fontPackDir.string();
        std::invalid_argument e(msg.c_str());

        std::wcerr << e.what() << std::endl;

        throw e;
    }

    std::filesystem::path sysFontPath(SYS_FONT_PATH_W);
    std::filesystem::path usrFontPath(USR_FONT_PATH_W);

    this->isInstalled = true;

    if (fontPackDir.parent_path() == sysFontPath)
    {
        this->type = installType::SYSTEM_INSTALL;
    }
    else if (fontPackDir.parent_path() == usrFontPath)
    {
        this->type = installType::USER_INSTALL;
    }
    else
    {
        this->type = installType::REMOVE_PACK;

        if (std::filesystem::exists(fontPackDir))
        {
            this->isInstalled = true;
        }
        else
        {
            std::wcout << L"The font package path co not exist. Path: " << fontPackDir.wstring() << std::endl;
        }
    }

    this->path = fontPackDir;
    this->packName = fontPackDir.filename().wstring();
}

fontPack::~fontPack()
{
    std::wcout << L"Removed package: " << this->packName << std::endl;
}

void fontPack::install()
{

}

void fontPack::remove()
{

}

listPack fontPack::getPackInfo()
{
    listPack lp;

    lp.name = this->packName;
    lp.type = this->type;

    return lp;
}