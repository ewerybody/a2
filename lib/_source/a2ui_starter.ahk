; this is the script that becomes the a2ui.exe in root!
If (!A_IsCompiled)
{
    MsgBox a2ui_starter should only be run compiled!
    ExitApp
}

_init_check_settings()
a2_ahk := _init_get_autohotkey_exe()

Run, %a2_ahk% a2ui.ahk, %A_ScriptDir%\lib

Return ; -----------------------------------------------------------------------------
#include ..\a2init_check.ahk
