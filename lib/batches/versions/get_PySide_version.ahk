#include %A_ScriptDir%\..\..\a2dev_find_py.ahk
pydir := path_dirname(a2dev_get_py())
if (!pydir) {
    MsgBox 16, Could not get "pydir" from "path_dirname(a2dev_get_py())"
    ExitApp
}

; Lists all compatible versions, prefered verison top.
cores := ["PySide2\Qt5Core.dll", "PySide6\Qt6Core.dll"]

for _, rel_path in cores
{
    qtdll_path := pydir . "\Lib\site-packages\" . rel_path
    if (!FileExist(qtdll_path))
        Continue

    FileGetVersion, version, %qtdll_path%
    if version
        Break
}

if (!version) {
    msg := "Unable to find any of those:`n  "
    msg .= string_join(cores, "`n  ") . "`n"
    msg .= "Make sure at least one is installed!"
    MsgBox, 16, No PySide Found!, %msg%
} else
    FileAppend, %version%, *
