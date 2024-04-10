#include %A_ScriptDir%\..\..\_a2dev_find_py.ahk
#include %A_ScriptDir%\..\..\a2_globals.ahk
#include %A_ScriptDir%\..\..\Autohotkey\lib\string.ahk
#include %A_ScriptDir%\..\..\Autohotkey\lib\path.ahk
py_exe := a2dev_get_py()
if (!FileExist(py_exe))
    MsgBox("No Python Found here`n" . py_exe)

SplitPath py_exe,, &py_dir
FileAppend py_dir, "*"
