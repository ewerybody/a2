#Include  %A_ScriptDir%\..\path.ahk

p := A_ScriptFullPath
x := path_dirname(p)
y := path_dirname(x)
z := path_join(y, ["somedir", "readme.txt"])
sub_dir := "\..\..\ASD"
n := path_normalize(y sub_dir)
a1 := path_is_absolute(sub_dir)
a2 := path_is_absolute(n)
f1 := path_is_file(p)
f2 := path_is_file(z)
f3 := path_is_file(x)

d1 := path_is_dir(x)
d2 := path_is_dir(n)
b1 := path_basename(p)

msgbox a path: %p%`npath_dirname: %x%`npath_dirname: %y%`npath_join: %z%`npath_normalize: %n%`npath_is_absolute: %a1% (%sub_dir%)`npath_is_absolute: %a2% (%n%)`npath_is_file: %f1% (%p%)`npath_is_file: %f2% (%z%)`npath_is_file: %f3% (%x%)`npath_is_dir: %d1% (%x%)`npath_is_dir: %d2% (%n%)`npath_basename: %b1% (%p%)
