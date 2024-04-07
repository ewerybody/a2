#Include ..\..\..\a2_globals.ahk
#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include path.ahk
#Include string.ahk

p := A_ScriptFullPath
x := path_dirname(p)
y := path_dirname(x)
z := path_join(y, "somedir", "readme.txt")
p2 := path_join(y, path_basename(x), A_ScriptName)
sub_dir := "\..\..\ASD"
n := path_normalize(y sub_dir)
a1 := assertmsg(!path_is_absolute(sub_dir))
a2 := assertmsg(path_is_absolute(n))
f1 := assertmsg(path_is_file(p))
f2 := assertmsg(!path_is_file(z))
f3 := assertmsg(!path_is_file(x))
f4 := assertmsg(path_is_file(p2))

d1 := assertmsg(path_is_dir(x))
d2 := assertmsg(!path_is_dir(n))
b1 := path_basename(p)

e0 := assertmsg(!path_is_empty(A_ScriptDir))
test_dir := A_ScriptDir "\_ emptytest39yfh32oufh"
DirCreate(test_dir)
e1 := assertmsg(path_is_empty(test_dir))
DirDelete(test_dir)

write_test_file := path_join(A_ScriptDir, "write_test_file")
path_set_writable(write_test_file)
FileAppend(write_test_file, write_test_file)
path_set_readonly(write_test_file)
w1 := assertmsg(!path_is_writeable(write_test_file))
path_set_writable(write_test_file)
w2 := assertmsg(path_is_writeable(write_test_file))
FileDelete(write_test_file)

epth := "%SystemRoot%\System32\imageres.dll"
npth := path_expand_env(epth)
x1 := assertmsg(InStr(npth, "%") == 0)
x2 := assertmsg(FileExist(npth))

base_ext := path_split_ext(A_ScriptFullPath)
sx1 := assertmsg("test_path" == base_ext[1])
sx2 := assertmsg("ahk" == base_ext[2])

; Test path_get_free_name
FileAppend("", A_ScriptDir . "\_test_file.txt")
Loop(3)
    FileAppend("", A_ScriptDir . "\_test_file" . A_Index . ".txt")
Sleep(100)
found_name := path_get_free_name(A_ScriptDir, "_test_file", "txt")
fn := assertmsg(found_name == "_test_file4")
; test with separator
found_name := path_get_free_name(A_ScriptDir, "_test_file", "txt", "__")
fns := assertmsg(found_name == "_test_file__2")
; cleanup
Loop(3)
    FileDelete(A_ScriptDir . "\_test_file" . A_Index . ".txt")
FileDelete(A_ScriptDir . "\_test_file.txt")
found_name := path_get_free_name(A_ScriptDir, "", "")
fn2 := assertmsg(!found_name)

msg := "a path: " p "`npath_dirname: " x "`npath_dirname: " y "`npath_join: " z "`n`n"
msg .= "path_normalize: " n "`n!path_is_absolute: " a1 "(" sub_dir ")`npath_is_absolute: " a2 "(" n ")`n`n"
msg .= "path_is_file: " f1 "(" p ")`n!path_is_file: " f2 "(" z ")`n!path_is_file: " f3 "(" x ")`npath_is_file: " f4 "(" p2 ")`n`n"
msg .= "path_is_dir: " d1 " (" x ")`n!path_is_dir: " d2 " (" n ")`npath_basename: " b1 " (" p ")`n`n"
msg .= "!path_is_empty: " e0 " (" A_ScriptDir ")`npath_is_empty: " e1 " (" test_dir ")`n`n"
msg .= "!path_is_writeable: " w1 "`npath_is_writeable: " w2 "`n"
msg .= "path_expand_env: " x1 " " x2 "`n"
msg .= "path_split_ext: " sx1 " " sx2 " '" base_ext[1] "' '" base_ext[2] "'`n"
msg .= "path_free_name: " fn " " fn2 " " fns
msgbox(msg)
