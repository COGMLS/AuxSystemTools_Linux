###########################################################
#
# CMakeLists: Linux Image Backup Solution
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
set(LinuxImageBackupReposRoot ${CMAKE_CURRENT_LIST_DIR})

# Set the Final Binary Output to build the separated from other projects during the compilation:
#set(UseLinuxImageBackupLocalFinalBinDir True)

if (UseLinuxImageBackupLocalFinalBinDir)
	set(LinuxImageBackupFinalBinDir "${LinuxImageBackupReposRoot}/build/bin")
	set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${LinuxImageBackupFinalBinDir})
	if (NOT WIN32)
		set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${LinuxImageBackupFinalBinDir})
	endif()
	#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${LinuxImageBackupFinalBinDir})
endif()

# Define the DEBUG preprocessor definition:
set(DebugLinuxImageBackup True)

project(
			LinuxImageBackupProject
			VERSION 1.0.0
			DESCRIPTION "Linux Image Backup solution with a console for tests."
		)

###########################################################
#
# Sub projects:
#
###########################################################

add_subdirectory("Console")