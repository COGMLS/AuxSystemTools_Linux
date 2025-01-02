###########################################################
#
# CMakeLists: Linux Image Backup standalone tool
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

# Define if is Windows Environment:

if(WIN32)
	add_compile_definitions(WIN32)
endif()

if(WIN32)
	add_compile_definitions(_CONSOLE)
endif()

if(DebugLinuxImageBackup)
	add_compile_definitions(DEBUG)
	enable_testing()
endif()

add_compile_definitions(UNICODE)
add_compile_definitions(_UNICODE)

# Defined the project:
project(
			LinuxImageBackupTool
			VERSION 1.0.0
			DESCRIPTION "Linux Image Backup standalone tool"
		)

###########################################################
#
# Project components settings:
#
###########################################################

# Include libraries directories source codes:
include_directories("{LinuxImageBackupReposRoot}/Console/ToolSrc/ImageTool")
include_directories("{LinuxImageBackupReposRoot}/Console/ToolSrc/DiskTools")

# Define the executable properties:
add_executable(
					LinuxImageBackupTool
					"main.cpp"
				)

# Define manual library link:
set(UseManualTargetLinkLibs False)
				
# Link the LinuxImageBackup:
if(UseManualTargetLinkLibs)
	if (WIN32)
		if(DebugLinuxImageBackup)
			#target_link_libraries(LinuxImageBackupTool ${ReposRoot}/build/LinuxImageBackup/Libs/<lib>/Debug/<libName>.lib)
		else()
			#target_link_libraries(LinuxImageBackupTool ${ReposRoot}/build/LinuxImageBackup/Libs/<lib>/Release/<libName>.lib)
		endif()
	else()
		#target_link_libraries(LinuxImageBackupTool ${ReposRoot}/build/bin/lib<libName>.so)
	endif()
else()
	#target_link_libraries(LinuxImageBackupTool <libName>)
endif()

# Enable tests if DEBUG is set:

if (DEBUG)
endif()