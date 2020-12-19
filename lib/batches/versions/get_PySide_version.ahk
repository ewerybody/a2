#include ..\a2dev_find_py.ahk
pydir := path_dirname(a2dev_get_py())
qtdll_path := pydir "\Lib\site-packages\PySide6\Qt6Core.dll"
if (!FileExist(qtdll_path))
    MsgBox, No Qt DLL Found here`n%qtdll%`nIs PySide6 installed?!?!
FileGetVersion, version, %qtdll_path%
if (!version)
    MsgBox, No Qt DLL Version found!`n%qtdll_path%
FileAppend, %version%, *
