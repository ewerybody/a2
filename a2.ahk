#SingleInstance force
#Persistent
; a2 - modular Autohotkey script envirionment
; main file! This basically gathers all resources

tt("a2 started!",1)

; TODO: make this optional
SetTitleMatchMode, 2

; load variables
#include settings\variables.ahk
; init phase
;Gosub, a2Init

Return ; -------------------------------------------------------------------------------------------

; load libraries
#include settings\libs.ahk
; load the selected functionalities
#include settings\includes.ahk
; load according hotkeys for those ; standard hotkeys configurable through this include too
#include settings\hotkeys.ahk
; for things that need an initiation phase
#include settings\init.ahk

a2UI() {
    ; TODO: placeholder. call PySide a2ui when available
    tt("a2ui...", 0.5)
    Run, C:\Python34\pythonw.exe a2ui.py, %A_ScriptDir%\ui\
    ;Run, C:\Python34\python.exe a2ui.py, %A_ScriptDir%\ui\
    ;Run, pythonw.exe %A_ScriptDir%\ui\a2ui.py, C:\Python34
}
