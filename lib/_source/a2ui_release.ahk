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

a2tip("Calling a2 ui ...")
Run, ui\pythonw.exe ui\a2app.py
sleep, 1000
ExitApp

Return ; -----------------------------------------------------------------------------
#include ..\Autohotkey\lib\a2tip.ahk
#include ..\Autohotkey\lib\font.ahk