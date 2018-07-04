; a2 - modular Autohotkey script envirionment
; main file! This basically gathers all resources
#SingleInstance force
#Persistent
#NoTrayIcon
SetWorkingDir %A_ScriptDir%\..
a2Dir := A_ScriptDir "\.."
#include settings\a2_settings.ahk
#include lib\Globals.ahk
#include lib\_defaults\a2_urls.ahk

Menu, Tray, Icon, %UIresources%\a2.ico, , 1
Menu, Tray, Icon
Gui, 1:Destroy

Menu, Tray, NoStandard
Menu, Tray, DeleteAll
Menu, Tray, Tip, %a2_title%
Menu, Tray, Click, %a2_tray_click_button% ;makes the menu act on standard "left" click
Menu, Tray, add, open a2 user interface, a2ui
Menu, Tray, icon, open a2 user interface, %UIresources%\a2.ico
Menu, Tray, default, open a2 user interface
Menu, Tray, add, reload a2, a2ui_reload
Menu, Tray, icon, reload a2, %UIresources%\a2reload.ico
Menu, Tray, add, help on a2, a2ui_help
Menu, Tray, icon, help on a2, %UIresources%\a2help.ico
Menu, Tray, add, quit a2, a2ui_exit
Menu, Tray, icon, quit a2, %UIresources%\a2x.ico

if a2_startup_tool_tips
    tt(a2_title, 1)

#include %A_ScriptDir%\..\settings\a2_init.ahk
Return ; -----------------------------------------------------------------------------

a2UI:
    a2UI()
Return
a2ui() {
    global a2_ahk
    ifNotExist, %a2_ahk%
        a2_ahk = %A_ScriptDir%\Autohotkey\Autohotkey.exe
    Run, "%a2_ahk%" "%A_ScriptDir%\a2ui.ahk", %A_ScriptDir%
}

a2ui_help:
    Run, %a2_help%
Return
a2ui_reload:
    Reload
Return
a2ui_exit:
    ExitApp
Return
