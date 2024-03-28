#include "listPack.hpp"

void printList(std::vector<listPack> &list, unsigned int maxWidth = 30)
{
    std::wstring header = L"";
    std::wstring headerNames = L"";

    unsigned int i = 0;
    unsigned int namei = 0u;
    unsigned int nameSize = maxWidth * 0.75;
    unsigned int typeSize = maxWidth * 0.25;
    
    bool bNameHeader = true;
    bool bTypeHeader = true;
    
    headerNames += L" Pack Name";
    namei = headerNames.size();

    for (i = 0; i < maxWidth; i++)
    {
        if (namei >= nameSize && bNameHeader)
        {
            bNameHeader = false;
        }

        if (bNameHeader)
        {
            headerNames += L' ';
            namei++;
        }

        if (!bNameHeader)
        {
            if (bTypeHeader)
            {
                std::wstring tmpType = L"Install Type";
                headerNames += tmpType;
                namei += tmpType.size();
                bTypeHeader = false;
            }
            else
            {
                headerNames += L' ';
                namei++;
            }
        }

        header += L'-';
    }

    unsigned int iMax = list.size();
    i = 0u;

    std::wcout << headerNames << std::endl;
    std::wcout << header << std::endl;

    while (i < iMax)
    {
        // Pack Name ... Install Type
        try
        {
            std::wcout << list.at(i).name;

            for (unsigned int j = 0; j < nameSize; j++)
            {
                std::wcout << L' ';
            }
            
            if (list.at(i).type == installType::USER_INSTALL)
            {
                std::wcout << USR_INSTALL_W;
            }
            else
            {
                std::wcout << SYS_INSTALL_W;
            }

            std::wcout << std::endl;
        }
        catch(const std::exception& e)
        {
            std::wcerr << e.what() << std::endl;
        }

        i++;
    }
}