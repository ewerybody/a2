; a2 - modular Autohotkey script envirionment
; main file! This gathers all the runtime resources
#SingleInstance force
#Persistent
#NoTrayIcon

#include <ahk_functions>
; #include <a2functions>
#include lib\a2_config.ahk
#include lib\a2_globals.ahk
#include lib\a2_urls.ahk
#include *i %A_AppData%\..\Local\a2\data\a2_data_path.ahk
#include *i lib\a2_portable.ahk

; build essential paths
a2dir := A_ScriptDir "\..\"
SetWorkingDir %a2dir%
a2ui_res := a2dir "ui\res\"

If !a2data {
    EnvGet, a2data, LOCALAPPDATA
    a2data := a2data "\a2\data\"
}
If !string_endswith(a2data, "\")
    a2data := a2data "\"

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
Menu, Tray, Click, 1
Menu, Tray, add, Open a2 User Interface, a2ui
Menu, Tray, icon, Open a2 User Interface, %a2ui_res%a2.ico
Menu, Tray, default, Open a2 User Interface
Menu, Tray, add, Open a2 Directory, a2_explore
Menu, Tray, icon, Open a2 Directory, %a2ui_res%a2.ico
Menu, Tray, add, Reload a2 Runtime, a2ui_reload
Menu, Tray, icon, Reload a2 Runtime, %a2ui_res%a2reload.ico
Menu, Tray, add, Help on a2, a2ui_help
Menu, Tray, icon, Help on a2, %a2ui_res%a2help.ico
Menu, Tray, add, Quit a2 Runtime, a2ui_exit
Menu, Tray, icon, Quit a2 Runtime, %a2ui_res%a2x.ico

if a2_startup_tool_tips
    tt(a2_title, 1)

; Finally the user data includes happening in the end so the top of this main script
; is executed before the first Return.
#include *i lib\_ user_data_includes.ahk
Return ; -----------------------------------------------------------------------------

a2ui() {
    tt("Calling a2 ui ...")
    a2_ahk = %A_ScriptDir%\Autohotkey\Autohotkey.exe
    Run, "%a2_ahk%" "%A_ScriptDir%\a2ui.ahk", %A_ScriptDir%
    WinWait, a2,, 5
    tt("Calling a2 ui ...", 1)
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

a2_explore:
    Run, %A_WinDir%\explorer.exe %a2dir%
Return
