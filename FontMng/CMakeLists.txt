###########################################################
#
# CMakeLists: Font Manager for Linux
#
###########################################################

cmake_minimum_required(VERSION 3.12.0)

###########################################################
#
# Define the general solution settings
#
###########################################################

# Define the project C++ version:
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED true)

# Define the project's name:
project(FontMng VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

add_executable(
				FontMng.app
				"constants.hpp"
				"globalData.hpp"
				"commands.hpp" "commands.cpp"
				"main.cpp"
				"fontPack.hpp" "fontPack.cpp"
				"listPack.hpp" "listPack.cpp"
				)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
