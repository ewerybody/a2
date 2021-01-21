; this is the script that becomes the a2ui.exe in root!
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico

#Persistent
If (!A_IsCompiled)
{
    MsgBox, 16, ERROR, a2ui_starter should only be run compiled!
    ExitApp
}

tt("Calling a2 ui ...")
a2_ahk := _init_get_autohotkey_exe()

Run, %a2_ahk% a2ui.ahk, %A_ScriptDir%\lib
tt("Calling a2 ui ...", 1,,1)

Return ; -----------------------------------------------------------------------------
#include ..\a2init_check.ahk
#include ..\Autohotkey\lib\tt.ahk
