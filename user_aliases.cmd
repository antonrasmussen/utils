;= @echo off
;= rem Call DOSKEY and use this file as the macrofile
;= %SystemRoot%\system32\doskey /listsize=1000 /macrofile=%0%
;= rem In batch mode, jump to the end of the file
;= goto:eof
;= Add aliases below here
e.=explorer .
gl=git log --oneline --all --graph --decorate  $*
ls=ls --show-control-chars -F --color $*
pwd=cd
clear=cls
history=cat "%CMDER_ROOT%\config\.history"
unalias=alias /d $1
vi=vim $*
cmderr=cd /d "%CMDER_ROOT%"
l=ls -ltrah --show-control-chars -F --color $*  
repos=cd C:\repos\  
root=cd C:\
zilla="C:\programs\cmder\vendor\filezilla\FileZilla-3.39.0\filezilla.exe" $* -new_console:s75H
unalias=alias /d $1
vi=vim $*
~=cd C:/
editAlias=echo sub C:\programs\cmder\config\user_aliases.cmd
scifi=cd C:\programs\scala
sub="C:\programs\cmder\vendor\sublime\sublime_text.exe" $*
pyfi=cd C:\pyFiles
