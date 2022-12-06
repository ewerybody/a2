; Becomes `a2ui.exe` in the root of our DEV environment.
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico
;@Ahk2Exe-SetCompanyName a2
;@Ahk2Exe-SetCopyright GPLv3
;@Ahk2Exe-SetDescription a2 ui starter - dev
;@Ahk2Exe-SetOrigFilename a2ui.exe
;@Ahk2Exe-SetProductName a2
;@Ahk2Exe-SetVersion 0.4.6
#NoTrayIcon
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

; Run, "%python%" "%script%"
cmd := """" python """ """ script """"
shell := ComObjCreate("WScript.Shell")
exec := shell.Exec(cmd)
; Is this SWITCHED? Why?
errors := exec.StdOut.ReadAll()
; For some reason standart-out-messages here come from StdErr!
; Well, since this is dev. Let's not worry about it too much ;)
; msg := exec.StdErr.ReadAll()
; if (msg)
;     msgbox_info(msg, "messages starting a2app")

if (errors)
    msgbox_error(errors, "ERROR starting a2app")
sleep, 1000
ExitApp

Return ; -----------------------------------------------------------------------------
#include ..\Autohotkey\lib\a2tip.ahk
#include ..\Autohotkey\lib\font.ahk
#include ..\Autohotkey\lib\msgbox.ahk
#include ..\_a2dev_find_py.ahk
