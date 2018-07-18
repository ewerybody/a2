#Include  %A_ScriptDir%\..\file_dirname.ahk

p := A_ScriptFullPath
x := file_dirname(p)
y := file_dirname(x)
msgbox p: %p%`nx: %x%`ny: %y%
