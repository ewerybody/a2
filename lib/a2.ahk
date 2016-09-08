; a2 - modular Autohotkey script envirionment
; main file! This basically gathers all resources
#SingleInstance force
#Persistent
#NoTrayIcon
#include %A_ScriptDir%\..\settings\a2_settings.ahk
#include _defaults\a2_urls.ahk

script_title := "a2"
icon_path = %A_ScriptDir%\..\ui\res
script_icon = %icon_path%\a2.ico
reload_icon = %icon_path%\a2reload.ico
close_icon = %icon_path%\a2x.ico
help_icon = %icon_path%\a2help.ico

Menu, Tray, Icon, %script_icon%, %script_icon#%, 1
Menu, Tray, Icon
Gui, 1:Destroy

Menu, Tray, NoStandard
Menu, Tray, DeleteAll
Menu, Tray, Tip, %script_title%
Menu, Tray, Click, %a2_tray_click_button% ;makes the menu act on standard "left" click
Menu, Tray, add, open a2 user interface, a2ui
Menu, Tray, icon, open a2 user interface, %script_icon%
Menu, Tray, default, open a2 user interface
Menu, Tray, add, reload a2, a2ui_reload
Menu, Tray, icon, reload a2, %reload_icon%
Menu, Tray, add, help on a2, a2ui_help
Menu, Tray, icon, help on a2, %help_icon%
Menu, Tray, add, quit a2, a2ui_exit
Menu, Tray, icon, quit a2, %close_icon%

if a2_startup_tool_tips
    tt("a2 started!", 1)

#include %A_ScriptDir%\..\settings\a2_init.ahk
Return ; -------------------------------------------------------------------------------------------

a2UI:
    a2UI()
Return
a2ui() {
    global a2_ahk
    Run, %a2_ahk% a2ui.ahk
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
