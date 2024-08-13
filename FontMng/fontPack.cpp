#include "fontPack.hpp"

fontPack::fontPack(std::filesystem::path fontPackDir)
{
    // Verify if the path exist:
    if (!std::filesystem::exists(fontPackDir))
    {
        std::string msg = "The path \"" + fontPackDir.string() + "\" doesn't exist!";
        std::invalid_argument e(msg.c_str());
        throw e;
    }

    // Test the path if is a directory:
    if (!std::filesystem::is_directory(fontPackDir))
    {
        std::string msg = "Only a directory package can be used. Path: ";
        msg += fontPackDir.string();
        std::invalid_argument e(msg.c_str());

        //std::wcerr << e.what() << std::endl;

        throw e;
    }

    bool isSysFont = false;

    if (fontPackDir.wstring().starts_with(SYS_FONT_PATH_W))
    {
        isSysFont = true;
    }
    else if (!fontPackDir.wstring().starts_with(USR_FONT_PATH_W))
    {
        std::string msg = "The given path directory is not part of User of System font managed! Path: ";
        msg += fontPackDir.string();
        std::invalid_argument e(msg.c_str());

        throw e;
    }

    this->packPath = fontPackDir;
    this->packName = fontPackDir.filename().wstring();

    if (isSysFont)
    {
        this->type = installType::SYSTEM_INSTALL;
    }
    else
    {
        this->type = installType::USER_INSTALL;
    }

    std::list<std::wstring> fonts = getFontsList(isSysFont, true);

    auto installedFont = std::find(fonts.begin(), fonts.end(), this->packName);

    if (*installedFont == this->packName)
    {
        this->isInstalled = true;
    }
    else
    {
        this->isInstalled = false;
    }
}

fontPack::fontPack(std::filesystem::path fontPackDir, bool sysInstall)
{
    // Verify if the path exist:
    if (!std::filesystem::exists(fontPackDir))
    {
        std::string msg = "The path \"" + fontPackDir.string() + "\" doesn't exist!";
        std::invalid_argument e(msg.c_str());
        throw e;
    }
    
    // Test the path if is a directory:
    if (!std::filesystem::is_directory(fontPackDir))
    {
        std::string msg = "Only a directory package can be used. Path: ";
        msg += fontPackDir.string();
        std::invalid_argument e(msg.c_str());

        //std::wcerr << e.what() << std::endl;

        throw e;
    }

    this->packPath = fontPackDir;
    this->packName = fontPackDir.filename().wstring();

    if (sysInstall)
    {
        this->type = installType::SYSTEM_INSTALL;
    }
    else
    {
        this->type = installType::USER_INSTALL;
    }

    std::list<std::wstring> fonts = getFontsList(sysInstall, true);

    auto installedFont = std::find(fonts.begin(), fonts.end(), this->packName);

    if (*installedFont == this->packName)
    {
        this->isInstalled = true;
    }
    else
    {
        this->isInstalled = false;
    }
}

fontPack::~fontPack()
{
    
}

int fontPack::install()
{
    if (!this->isInstalled)
    {
        std::filesystem::path installPath;
        std::error_code errorCode;

        if (this->type == installType::SYSTEM_INSTALL)
        {
            installPath = SYS_FONT_PATH_W;
        }
        else
        {
            installPath = USR_FONT_PATH_W;
        }

        if (!this->isInstalled)
        {
            try
            {
                std::filesystem::copy(this->packPath, installPath, errorCode);
                this->isInstalled = true;
                return 1;
            }
            catch(const std::exception& e)
            {
                std::wcerr << e.what() << '\n';
                return -1;
            }
        }
    }

    return 0;
}

int fontPack::remove()
{
    if (this->isInstalled)
    {
        std::filesystem::path removePath;
        std::error_code errorCode;

        try
        {
            std::filesystem::remove(this->packPath, errorCode);
            this->isInstalled = false;
            return 1;
        }
        catch(const std::exception& e)
        {
            std::cerr << e.what() << '\n';
            return -1;
        }
    }

    return 0;
}

listPack fontPack::getPackInfo()
{
    listPack lp;

    lp.name = this->packName;
    lp.type = this->type;
    lp.installed = this->isInstalled;

    return lp;
}