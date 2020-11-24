#Include  %A_ScriptDir%\..\path.ahk


assert(things) {
    if things
        return "✔"
    Return "❌"
}

p := A_ScriptFullPath
x := path_dirname(p)
y := path_dirname(x)
z := path_join(y, ["somedir", "readme.txt"])
sub_dir := "\..\..\ASD"
n := path_normalize(y sub_dir)
a1 := assert(!path_is_absolute(sub_dir))
a2 := assert(path_is_absolute(n))
f1 := assert(path_is_file(p))
f2 := assert(!path_is_file(z))
f3 := assert(!path_is_file(x))

d1 := assert(path_is_dir(x))
d2 := assert(!path_is_dir(n))
b1 := path_basename(p)

e0 := assert(!path_is_empty(A_ScriptDir))
test_dir := A_ScriptDir "\_ emptytest39yfh32oufh"
FileCreateDir, %test_dir%
e1 := assert(path_is_empty(test_dir))
FileRemoveDir, %test_dir%

write_test_file := path_join(A_ScriptDir, ["write_test_file"])
path_set_writable(write_test_file)
FileAppend, write_test_file, %write_test_file%
path_set_readonly(write_test_file)
w1 := assert(!path_is_writeable(write_test_file))
path_set_writable(write_test_file)
w2 := assert(path_is_writeable(write_test_file))
FileDelete, %write_test_file%

msg = a path: %p%`npath_dirname: %x%`npath_dirname: %y%`npath_join: %z%`n`n
msg = %msg%path_normalize: %n%`n!path_is_absolute: %a1% (%sub_dir%)`npath_is_absolute: %a2% (%n%)`n`n
msg = %msg%path_is_file: %f1% (%p%)`n!path_is_file: %f2% (%z%)`n!path_is_file: %f3% (%x%)`n`n
msg = %msg%path_is_dir: %d1% (%x%)`n!path_is_dir: %d2% (%n%)`npath_basename: %b1% (%p%)`n`n
msg = %msg%!path_is_empty: %e0% (%A_ScriptDir%)`npath_is_empty: %e1% (%test_dir%)`n`n
msg = %msg%!path_is_writeable: %w1%`npath_is_writeable: %w2%
msgbox %msg%
