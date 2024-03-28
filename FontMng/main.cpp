#include "pch.h"

#include "fontPack.hpp"

int main(int argc, const char* argv[])
{
    std::locale loc("en_US.UTF-8");

    std::locale::global(loc);

    std::cout << "Hello, from FontMng!\n";

    std::string s = "\n";

    std::cout << "Press enter to continue...";
    std::cin >> s;

    return 0;
}
