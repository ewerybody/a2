; a2 - modular Autohotkey script envirionment
; main file! This basically gathers all resources
#SingleInstance force
#Persistent
#NoTrayIcon

a2dir := A_ScriptDir "\..\"
SetWorkingDir %a2dir%
a2ui_res := a2dir "ui\res\"
EnvGet, a2data, LOCALAPPDATA
a2data := a2data "\a2\data\"

#include <ahk_functions>
#include <a2functions>
#include lib\a2_config.ahk
#include lib\a2_globals.ahk
#include lib\a2_urls.ahk

Menu, Tray, Icon, %a2ui_res%a2.ico, , 1
Menu, Tray, Icon
Gui, 1:Destroy

Menu, Tray, NoStandard
Menu, Tray, DeleteAll
Menu, Tray, Tip, %a2_title%
Menu, Tray, Click, %a2_tray_click_button% ;makes the menu act on standard "left" click
Menu, Tray, add, open a2 user interface, a2ui
Menu, Tray, icon, open a2 user interface, %a2ui_res%a2.ico
Menu, Tray, default, open a2 user interface
Menu, Tray, add, reload a2, a2ui_reload
Menu, Tray, icon, reload a2, %a2ui_res%a2reload.ico
Menu, Tray, add, help on a2, a2ui_help
Menu, Tray, icon, help on a2, %a2ui_res%a2help.ico
Menu, Tray, add, quit a2, a2ui_exit
Menu, Tray, icon, quit a2, %a2ui_res%a2x.ico

if a2_startup_tool_tips
    tt(a2_title, 1)

#include *i %a2data%a2_init.ahk
Return ; -----------------------------------------------------------------------------

a2ui() {
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
