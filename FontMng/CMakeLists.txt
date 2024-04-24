cmake_minimum_required(VERSION 3.12.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED true)

project(FontMng VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

add_executable(FontMng.app main.cpp fontPack.cpp listPack.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
