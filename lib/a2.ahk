; a2 - modular Autohotkey script envirionment
; main file! This gathers all the runtime resources
#SingleInstance force
#Persistent
#NoTrayIcon

#include <ahk_functions>
#include <a2functions>
#include lib\a2_config.ahk
#include lib\a2_globals.ahk
#include lib\a2_urls.ahk

; build essential paths
a2dir := A_ScriptDir "\..\"
SetWorkingDir %a2dir%
a2ui_res := a2dir "ui\res\"

If !a2data {
    EnvGet, a2data, LOCALAPPDATA
    a2data := a2data "\a2\data\"
}
global a2modules := a2data "modules\"
global a2module_data := a2data "module_data\"
global a2includes := a2data "includes\"
global a2temp := a2data "temp\"
global a2db := a2data "ad.db"

; build the tray icon menu
Menu, Tray, Icon, %a2ui_res%a2.ico, , 1
Menu, Tray, Icon
Gui, 1:Destroy

Menu, Tray, NoStandard
Menu, Tray, DeleteAll
Menu, Tray, Tip, %a2_title%
Menu, Tray, Click, %a2_tray_click_button%
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

; Finally the user data includes happening in the end so the top of this main script
; is executed before the first Return.
#include *i lib\_user_data_includes.ahk
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
