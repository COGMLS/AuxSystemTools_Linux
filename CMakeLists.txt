###########################################################
#
# CMakeLists: AuxSystemTools for Linux Solution
#
###########################################################

cmake_minimum_required(VERSION 3.12.0)

###########################################################
#
# Define the general solution settings
#
###########################################################

# Define the global C/C++ standard used:
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED true)

# Define final location for binary files output:
set(ReposRoot ${CMAKE_CURRENT_LIST_DIR})
set(FinalBinDir "${ReposRoot}/build/bin")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${FinalBinDir})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${FinalBinDir})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${FinalBinDir})

# Define the main solution:
project("AuxSystemTools for Linux")

###########################################################
#
# Sub projects:
#
###########################################################

add_subdirectory("FontMng")