; this is the script that becomes the a2ui.exe in root!
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico
;@Ahk2Exe-SetCompanyName a2
;@Ahk2Exe-SetCopyright GPLv3
;@Ahk2Exe-SetDescription a2 ui starter
;@Ahk2Exe-SetOrigFilename a2ui.exe
;@Ahk2Exe-SetProductName a2
;@Ahk2Exe-SetVersion 0.3.0

#Persistent
If (!A_IsCompiled)
{
    MsgBox, 16, ERROR, a2ui_starter should only be run compiled!
    ExitApp
}

tt("Calling a2 ui ...")
a2_ahk := _init_get_autohotkey_exe()

Run, %a2_ahk% a2ui.ahk, %A_ScriptDir%\lib
a2tip("Calling a2 ui ...")
sleep, 1000
ExitApp

Return ; -----------------------------------------------------------------------------
#include ..\a2init_check.ahk
#include ..\Autohotkey\lib\a2tip.ahk
