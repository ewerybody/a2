#include %A_ScriptDir%\..\..\a2dev_find_py.ahk
py_exe := a2dev_get_py()
if (!FileExist(py_exe))
    MsgBox, No Python Found here`n%py_exe%

SplitPath, py_exe,, py_dir
FileAppend, %py_dir%, *
