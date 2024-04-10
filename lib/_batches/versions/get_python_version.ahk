#include %A_ScriptDir%\..\..\_a2dev_find_py.ahk
#include %A_ScriptDir%\..\..\a2_globals.ahk
#include %A_ScriptDir%\..\..\Autohotkey\lib\string.ahk
#include %A_ScriptDir%\..\..\Autohotkey\lib\path.ahk
py := a2dev_get_py()
if (!FileExist(py))
    MsgBox("No Python Found here`n" . py)
version := FileGetVersion(py)
if (!version)
    MsgBox("No Python Version found!`n" . py)
FileAppend version, "*"
