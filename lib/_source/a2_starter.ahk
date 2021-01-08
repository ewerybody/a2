; this is the script that becomes the a2.exe in root!
If (!A_IsCompiled)
{
    MsgBox, 16, ERROR, a2_starter should ONLY be run compiled!
    ExitApp
}

a2_ahk := _init_get_autohotkey_exe()

Run, %a2_ahk% lib\a2.ahk

If !FileExist(A_ScriptDir "\_ user_data_include") {
    MsgBox A_ScriptDir: %A_ScriptDir%
    MsgBox, 65, a2 - First Start, Welcome! This a2 package does not seem to be started before`nand is not configured yet!`nThe Interface can be only opened through the Tray Icon or the a2ui executable.`n`nOr I can do that right now!
    IfMsgBox, Ok
        Run, "%a2_ahk%" a2ui.ahk, %A_ScriptDir%\lib
}

Return ; -----------------------------------------------------------------------------
#include ..\a2init_check.ahk
