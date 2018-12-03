#Include  %A_ScriptDir%\..\path.ahk

p := A_ScriptFullPath
x := path_dirname(p)
y := path_dirname(x)
msgbox p: %p%`nx: %x%`ny: %y%
