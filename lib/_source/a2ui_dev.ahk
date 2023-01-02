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
#SingleInstance, force
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

startup_log_path := ui_path "\_ startup_error.log"
if FileExist(startup_log_path)
    FileDelete, %startup_log_path%

a2tip("Calling a2 ui ...")
; We NEED to use `Run` to start detached and cannot collect output from python process!
; The call would need to wait as long as the ui is open!! This is a no-go!
; Startup Errors need to be handled by a2app!
Run, "%python%" "%script%", "%ui_path%"
sleep, 1000
if FileExist(startup_log_path) {
    msgbox_error(FileRead(startup_log_path), "Startup Error")
}
ExitApp

Return ; -----------------------------------------------------------------------------
#include ..\Autohotkey\lib\ahk_functions.ahk
#include ..\Autohotkey\lib\a2tip.ahk
#include ..\Autohotkey\lib\font.ahk
#include ..\Autohotkey\lib\msgbox.ahk
#include ..\_a2dev_find_py.ahk
