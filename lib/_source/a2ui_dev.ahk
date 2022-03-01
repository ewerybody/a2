; Becomes `a2ui.exe` in the root of our DEV environment.
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico
;@Ahk2Exe-SetCompanyName a2
;@Ahk2Exe-SetCopyright GPLv3
;@Ahk2Exe-SetDescription a2 ui starter - dev
;@Ahk2Exe-SetOrigFilename a2ui.exe
;@Ahk2Exe-SetProductName a2
;@Ahk2Exe-SetVersion 0.4.0

#Persistent
If (!A_IsCompiled) {
    MsgBox, 16, ERROR, a2ui starter should only be run compiled!
    ExitApp
}

ui_path := A_ScriptDir "\ui"
python := a2dev_get_py()
script := ui_path "\a2app.py"

for _, pth in [ui_path, python, script]
{
    if !FileExist(pth) {
        msgbox_error("Unable to startup the UI! Path is invalid:`n`n" pth)
        ExitApp
    }
}

a2tip("Calling a2 ui DEV ...")
Run, "%python%" "%script%"
sleep, 1000
ExitApp

Return ; -----------------------------------------------------------------------------
#include ..\Autohotkey\lib\a2tip.ahk
#include ..\Autohotkey\lib\font.ahk
#include ..\Autohotkey\lib\msgbox.ahk
#include ..\_a2dev_find_py.ahk
