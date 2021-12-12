#include %A_ScriptDir%\..\..\a2dev_find_py.ahk
py := a2dev_get_py()
if (!FileExist(py))
    MsgBox, No Python Found here`n%py%
FileGetVersion, version, %py%
if (!version)
    MsgBox, No Python Version found!`n%py%
FileAppend, %version%, *
