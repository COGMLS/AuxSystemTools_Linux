#include "pch.h"

#include "fontPack.hpp"

int main(int argc, const char* argv[])
{
    std::locale loc("en_US.UTF-8");

    std::locale::global(loc);

    std::wcout << "Font Package Manager for Linux\n";

    std::wstring usr = L"";

    while (usr != L"exit")
    {
        usr = L"";
        std::wcout << L"Use \"help\" for details. >";
        std::wcin >> usr;

        if (usr == L"hi")
        {
            std::wcout << "Say hi!" << std::endl;
        }
        else
        {
            std::wcout << L"Command not recognized! Make sure the command is only in lower case." << std::endl;
        }
    }

    return 0;
}
