; this is the script that becomes the a2.exe in root!
If (!A_IsCompiled)
{
    MsgBox a2_starter should only be run compiled!
    ExitApp
}

#include *i %A_AppData%\..\Local\a2\data\a2_data_path.ahk

_init_has_config_test() {
    global a2data
    If !a2data {
        EnvGet, a2data, LOCALAPPDATA
        a2data := a2data "\a2\data\"
    }
    IfExist, %a2data%\includes\hotkeys.ahk
        return true
    Else
        return false
}

a2_ahk := _init_get_autohotkey_exe()

Run, %a2_ahk% lib\a2.ahk

if !_init_has_config_test() {
    MsgBox, 65, a2 Not configured yet!, Welcome!`nThe a2 runtime is has no configuration yet! The Interface can be only opened through the Tray Icon or the a2ui executable.`n`nOr I can do that right now!
    IfMsgBox, Ok
        Run, "%a2_ahk%" a2ui.ahk, %A_ScriptDir%\lib
}

Return ; -----------------------------------------------------------------------------
#include ..\a2init_check.ahk

