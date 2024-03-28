#include "pch.h"

#include "fontPack.hpp"
#include <vector>

int main(int argc, const char* argv[])
{
    std::locale loc("en_US.UTF-8");
    std::locale::global(loc);

    std::vector<fontPack> list;

    std::wcout << "Font Package Manager for Linux\n";

    std::wstring usr = L"";

    std::wcout << L"Use \"help\" for details. >";
    while (std::getline(std::wcin, usr))
    {
        if (usr == L"exit")
        {
            break;
        }

        if (usr == L"hi")
        {
            std::wcout << "Say hi!" << std::endl;
        }
        else if (usr.starts_with(L"add "))
        {
            usr.erase(0, std::wstring(L"add ").size());

            if (usr.starts_with(L'\"') || usr.starts_with(L'\''))
            {
                usr.erase(0, 1);
            }
            
            if (usr.ends_with(L'\"') || usr.ends_with(L'\''))
            {
                usr.erase(usr.size() - 1, 1);
            }
            
            std::wstring tmp = usr;
            
            std::wcout << L"Adding path:" << tmp << std::endl;

            std::filesystem::path p(tmp);

            std::wcout << L"Path exists: " << std::filesystem::exists(p) << std::endl;
        }
        else
        {
            std::wcout << L"Command not recognized! Make sure the command is only in lower case." << std::endl;
        }

        std::wcout << L"Use \"help\" for details. >";
        usr = L"";
    }

    return 0;
}
