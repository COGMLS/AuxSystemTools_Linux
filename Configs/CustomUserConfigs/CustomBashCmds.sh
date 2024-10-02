# .CustomBashCmds.sh

#################################################
# Install instructions:
# -------------------------------
# To install the CustomBashCmds.sh
# is necessary edit the .bashrc file
# located in $HOME.
# Add the instruction:
# if [[ -f "$HOME/.CustomBashCmds.sh" ]]; then
#       . "$HOME/.CustomBashCmds.sh"
# fi
# NOTE: The instruction above can be
# placed in any part of the .bashrc
# file, but it's preferable to put in
# the end of file to avoid edit important
# bash definitions.
# 
# NOTE: The file CustomBashCmds.sh
# contains a dot on start the make it
# hidden. Edit the file's name putting a dot
# to make it hidden. Otherwise, use without
# dot on install instructions.
#################################################

#################################################
#
# Bash aliases:
#
#################################################

alias cls='clear'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
alias egrep='egrep --color=always'
alias fgrep='fgrep --color=always'
alias grep='grep --color=always'
alias nano='nano --linenumbers --autoindent --indicator'
alias nanov='nano --linenumbers --autoindent --indicator --view'

#################################################
#
# Git aliases:
#
#################################################

alias gitsync='git pull; git push'
alias gitsyncf='git fetch --verbose; git pull; git push'
alias gitgraph='git log --all --graph'

#################################################
#
# Apps aliases:
#
#################################################
