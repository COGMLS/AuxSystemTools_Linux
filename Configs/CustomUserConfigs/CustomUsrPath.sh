# .CustomUsrPath.sh

#######################################
# This file contains the custom PATH
# data for this user. To make it available
# for the user profile, set the in one of
# the files (~/.profile or ~/bash_profile)
# the follow instruction:
# 
# if [[ -f "$HOME/.CustomUsrPath.sh" ]]; then
# 	. "$HOME/CustomUsrPath.sh"
# fi
#
# IMPORTANT: If the file ~/bash_profile
# exists, the ~/.profile will not be read
# by the command interpreter.
# -------------------------------------
# How to set an additional value in the PATH:
#
# To add a new value inside the PATH, set
# a variable that will be available globally
# for the user profile and after that,
# add the variable into the PATH.
# 
# EXAMPLE:
# 
# # Create the variable and make it export:
# export DOTNET_ROOT=$HOME/dotnet
# # Add the variable into the PATH:
# export PATH=$PATH:$HOME/dotnet
#
# -------------------------------------
# To create an control to export or not
# a variable to PATH and void to edit
# to many lines, it's possible to create
# a local variable that controls the export
#
# EXAMPLE:
#
# # Enable the DOTNET_ROOT export:
# EXPORT_DOTNET_ROOT=true
#
# if [ "$EXPORT_DOTNET_ROOT" = true ]; then
# # Export the DOTNET_ROOT inside the statement
# fi
#
#######################################
