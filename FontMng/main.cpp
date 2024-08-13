#include "pch.h"

#include <unistd.h>

#include "fontPack.hpp"
#include "commands.hpp"
#include <vector>

int main(int argc, const char* argv[])
{
    bool isSystemCred = false;      // Detect if the user is using system credentials (as sudo)

    uid_t me = getuid();
    uid_t myPrivileges = geteuid();

    // If the current user is running with other user credentials and is not root, send a error message
    if (me != myPrivileges && me != 0)
    {
        return -1;
    }

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
            //help_cmd();
        }

        if (*c == CMDTYPE::ADD_CMD)
        {
            size_t i = 1;
            int argsAvailable = 0;
            bool isSystemCmd = false;
            std::vector<std::filesystem::path> args;

            if (cmds.size() >= 2)
            {
                if (cmds[1].getValue() == L"sys")
                {
                    isSystemCmd = true;
                    i = 2;
                }
            }

            while (i < cmds.size())
            {
                if (cmds[i] == CMDTYPE::ARGUMENT)
                {
                    argsAvailable++;
                    
                    std::wstring tmp = cmds[i].getValue();

                    if (tmp.starts_with(L'\"') || tmp.starts_with(L'\''))
                    {
                        tmp.erase(0, 1);
                    }
                    
                    if (tmp.ends_with(L'\"') || tmp.ends_with(L'\''))
                    {
                        tmp.erase(tmp.size() - 1, 1);
                    }

                    std::filesystem::path p(tmp);

                    if (std::filesystem::exists(p))
                    {
                        args.push_back(p);
                    }
                }
                else
                {
                    break;  // If a command was found assume the next arguments are to next cmd.
                }
                i++;
            }

            if (argsAvailable > 0)
            {
                if (argsAvailable != args.size())
                {
                    std::wcout << "One or more paths don't exist! They will be ignored." << std::endl;
                }

                std::vector<fontPack> fonts2Add;

                for (std::filesystem::path p : args)
                {
                    fonts2Add.push_back(fontPack(p, isSystemCmd));
                }

                std::wcout << L"\n\nList of fonts to install:" << std::endl;
                std::wcout << L"Installed | Install Type | Font pack name" << std::endl;

                for (i = 0; i < args.size(); i++)
                {
                    listPack listPackInfo = fonts2Add[i].getPackInfo();
                    std::wcout << listPackInfo.installed << L" | " << listPackInfo.type << L" | " << listPackInfo.name << std::endl;
                }

                std::wcout << L"\nConfirm to install these fonts (y/n): ";
                std::wstring usrConfirm;
                std::wcin >> usrConfirm;

                if (usrConfirm == L"y")
                {
                    listPack pack = fonts2Add[i].getPackInfo();
                    std::wcout << L"Installing " << pack.name << L"...";

                    if (fonts2Add[i].install() == 1)
                    {
                        std::wcout << "Installed" << std::endl;
                    }
                    else
                    {
                        std::wcout << "Failed" << std::endl;
                    }
                }
            }
            else
            {
                std::wcout << L"There are no arguments available for \"add\" command." << std::endl;
            }
        }

        if (*c == CMDTYPE::REMOVE_CMD)
        {

        }

        if (*c == CMDTYPE::LIST_CMD)
        {
            size_t i = 1;
            int argsAvailable = 0;
            bool isSystemCmd = false;

            if (cmds.size() >= 2)
            {
                if (cmds[1].getValue() == L"sys")
                {
                    isSystemCmd = true;
                    i = 2;
                }
            }

            std::filesystem::path baseFontPath = USR_FONT_PATH_W;

            if (isSystemCmd)
            {
                baseFontPath = SYS_FONT_PATH_W;
            }

            if (std::filesystem::exists(baseFontPath))
            {
                std::vector<fontPack> fontsList;

                for (std::filesystem::directory_entry d : std::filesystem::directory_iterator(baseFontPath))
                {
                    if (d.is_directory())
                    {
                        fontsList.push_back(fontPack(d.path()));
                    }
                }

                std::wcout << L"\n\nList of installed fonts:" << std::endl;
                std::wcout << L"Installed | Install Type | Font pack name " << std::endl;

                for (i = 0; i < fontsList.size(); i++)
                {
                    listPack listPackInfo = fontsList[i].getPackInfo();
                    std::wcout << listPackInfo.installed << L" | " << listPackInfo.type << L" | " << listPackInfo.name << std::endl;
                }

                std::wcout << "\n\n" << std::endl;

                //std::vector<listPack> listP;
                //for (size_t y = 0; y < fontsList.size(); y++)
                //{
                //    listP.push_back(fontsList[y].getPackInfo());
                //}
                //
                //printList(listP, 30);
            }
            else
            {
                std::wcout << L"The path to install/locate the fonts :" << baseFontPath << L" doesn't exist!" << std::endl;
            }
        }

        if (*c == CMDTYPE::ARGUMENT || *c == CMDTYPE::UNKNOWN_CMD)
        {
            std::wcout << L"Command not recognized! Make sure the command is only in lower case." << std::endl;
        }

        std::wcout << L"Use \"help\" for details. >";
        cmds.clear();
        usr = L"";
    }

    return 0;
}
