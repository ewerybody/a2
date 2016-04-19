#SingleInstance force
#Persistent
; a2 - modular Autohotkey script envirionment
; main file! This basically gathers all resources
#NoTrayIcon

ScriptTitle := "a2"
ScriptIcon = %A_ScriptDir%\ui\a2.ico

Menu, Tray, Icon, %ScriptIcon%, %ScriptIcon#%, 1
Menu, Tray, Icon
Gui, 1:Destroy
mainGuiID =

Menu, Tray, NoStandard
Menu, Tray, DeleteAll
Menu, Tray, Tip, %ScriptTitle%
Menu, Tray, Click, 1
Menu, Tray, add, open a2 user interface, a2UI
Menu, Tray, icon, open a2 user interface, %ScriptIcon%
Menu, Tray, default, open a2 user interface
Menu, Tray, add, reload a2, a2UI_reload
;%SystemRoot%\system32\imageres.dll,239
Menu, Tray, icon, reload a2, %ScriptIcon%
Menu, Tray, add, help on a2, a2UI_help
Menu, Tray, icon, help on a2, %SystemRoot%\system32\imageres.dll,95
Menu, Tray, add, quit a2, a2UI_exit
;%SystemRoot%\system32\imageres.dll,223
Menu, Tray, icon, quit a2, %ScriptIcon%

; TODO: make this optional
SetTitleMatchMode, 2

; load variables
#include settings\variables.ahk
; init phase
;Gosub, a2Init

tt("a2 started!",1)
Return ; -------------------------------------------------------------------------------------------

; load libraries
#include settings\libs.ahk
; load the selected functionalities
#include settings\includes.ahk
; load according hotkeys for those ; standard hotkeys configurable through this include too
#include settings\hotkeys.ahk
; for things that need an initiation phase
#include settings\init.ahk

a2UI:
    a2UI()
Return
a2UI() {
    ; TODO: placeholder. call PySide a2ui when available
    tt("a2ui...", 0.5)
    ;Run, C:\Python34\pythonw.exe a2app.py, %A_ScriptDir%\ui\
    Run, C:\Python34\python.exe a2app.py, %A_ScriptDir%\ui\
    ;Run, pythonw.exe %A_ScriptDir%\ui\a2ui.py, C:\Python34
}

a2UI_help:
    Run, https://github.com/ewerybody/a2#description
Return
a2UI_reload:
    Reload
Return
a2UI_exit:
    ExitApp
Return
