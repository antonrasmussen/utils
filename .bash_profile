export BASH_SILENCE_DEPRECATION_WARNING=1

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
#export PS1=" \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] :) "
export PS1="\[\033[32m\]\u@\h \w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] :) "

alias ll="ls -ltr"
alias repos="cd ~/repos"
alias vim="vi"

