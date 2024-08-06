#include "pch.h"

#include "fontPack.hpp"
#include "commands.hpp"
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
        std::vector<cmd> cmds = getCmdList(usr);

        cmd* c = &cmds[0];  // only the first "command" will be considered as a user command entry

        if (*c == CMDTYPE::EXIT_CMD)
        {
            break;
        }
        
        if (*c == CMDTYPE::HELP_CMD)
        {

        }

        if (*c == CMDTYPE::ADD_CMD)
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

        if (*c == CMDTYPE::REMOVE_CMD)
        {

        }

        if (*c == CMDTYPE::LIST_CMD)
        {
            std::vector<cmd> cmds = getCmdList(usr);

            std::wcout << L"Command List:" << std::endl;
            for (size_t i = 0; i < cmds.size(); i++)
            {
                std::wcout << L"[" << i << L"]::" << cmds[i] << std::endl;
            }
        }

        if (*c == CMDTYPE::ARGUMENT || *c == CMDTYPE::UNKNOWN_CMD)
        {
            std::wcout << L"Command not recognized! Make sure the command is only in lower case." << std::endl;
        }

        std::wcout << L"Use \"help\" for details. >";
        usr = L"";
    }

    return 0;
}
