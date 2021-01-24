; This is the script that becomes the a2.exe in root!
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico

If (!A_IsCompiled)
{
    MsgBox, 16, ERROR, a2_starter should ONLY be run compiled!
    ExitApp
}

a2_ahk := _init_get_autohotkey_exe()
if (A_Args.Length()) {
    args := _gather_args()
    Run, %a2_ahk% lib\a2.ahk %args%, %A_ScriptDir%
}
else
    Run, %a2_ahk% lib\a2.ahk, %A_ScriptDir%

If !FileExist(A_ScriptDir "\_ user_data_include") {
    ; Start the ui by default if there is no include file written yet.
    Run, "%a2_ahk%" a2ui.ahk, %A_ScriptDir%\lib
}

Return ; -----------------------------------------------------------------------
#include ..\a2init_check.ahk

_gather_args() {
    args := ""
    for _, arg in A_Args {
        if InStr(arg, A_Space) {
            args .= string_quote(arg) . " "
        }
        else
            args .= arg . " "
    }
    return args
}
