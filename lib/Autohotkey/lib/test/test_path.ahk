#Include  %A_ScriptDir%\..\path.ahk

p := A_ScriptFullPath
x := path_dirname(p)
y := path_dirname(x)
z := path_join(y, ["somedir", "readme.txt"])
n := path_normalize(y "\..\..\ASD")

msgbox a path: %p%`npath_dirname: %x%`npath_dirname: %y%`npath_join: %z%`npath_normalize: %n%
