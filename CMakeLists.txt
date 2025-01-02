###########################################################
#
# CMakeLists: Auxiliary System Tools for Linux Solution
#
###########################################################

cmake_minimum_required(VERSION 3.28)

###########################################################
#
# Define the general solution settings
#
###########################################################

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Define final location for binary files output:
set(ReposRoot ${CMAKE_CURRENT_LIST_DIR})
set(FinalBinDir "${ReposRoot}/build/bin")

#set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${FinalBinDir})

if(NOT WIN32)
	set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${FinalBinDir})
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${FinalBinDir})

# Auxiliary System Tools for Linux:
project(
			AuxSysTools4Linux
			VERSION 0.0.1
			DESCRIPTION "Complete solution for Auxiliary System Tools for Linux Solution repository."
		)

###########################################################
#
# Functions:
#
###########################################################

# Make a test with specific arguments:
function(mkArgTest test target arg)
	add_test(NAME ${test} COMMAND ${target} ${arg})
endfunction()

###########################################################
#
# Sub projects:
#
###########################################################

add_subdirectory("Tools")
#add_subdirectory("FontMng")