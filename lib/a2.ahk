; a2 - modular Autohotkey script envirionment
; main file! This gathers all the runtime resources
#SingleInstance force
#Persistent
#NoTrayIcon

#include <ahk_functions>
#include lib\a2_config.ahk
#include lib\a2_globals.ahk
#include lib\a2_urls.ahk

; build essential paths
global a2dir := A_ScriptDir "\..\"
SetWorkingDir %a2dir%
global a2ui_res := a2dir "ui\res\"
global a2lib := A_ScriptDir "\"

global a2data := _a2_get_data_path()
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

global a2cfg := _a2_get_user_config()

if !a2cfg.no_startup_tooltip
    tt(a2_title, 1)

if a2cfg.dev_mode
    SetTimer, a2_check_changes, 1000

; Finally the user data includes happening in the end so the top of this main script
; is executed before the first Return.
#include *i _ user_data_include
Return ; -----------------------------------------------------------------------------

a2ui() {
    tt("Calling a2 ui ...")
    a2_ahk := A_ScriptDir "\Autohotkey\Autohotkey.exe"
    Run, "%a2_ahk%" "%A_ScriptDir%\a2ui.ahk", %A_ScriptDir%
    WinWait, a2,, 5
    tt("Calling a2 ui ...", 1)
}

a2_check_changes() {
    ; Check library & module scripts for changes via archive file attribute.
    ; Removes the attribute from all files and returns true if any was found
    do_reload := false
    for _, libdir in [a2lib, path_join(a2lib, ["Autohotkey", "lib"])] {
        Loop, Files, %libdir%\*.ahk
        {
            If InStr(A_LoopFileAttrib, "A") {
                do_reload := true
                FileSetAttrib, -A, %A_LoopFileFullpath%
            }
        }
    }

    includes_path := path_join(a2data, ["includes", "includes.ahk"])
    Loop, read, %includes%
    {
        if !string_startswith(A_LoopReadLine, "#include ")
            Continue
        path := path_join(a2data, [SubStr(A_LoopReadLine, 10)])
        if InStr(FileGetAttrib(), "A") {
            do_reload := true
            FileSetAttrib, -A, %A_LoopFileFullpath%
        }
    }

    if do_reload
        a2ui_reload()
}

_a2_get_data_path() {
    ; Get the user data directory from cfg file or:
    ; Set it as "data", right in the the a2 root.
    user_include := "_ user_data_include"
    if !FileExist(user_include)
        return "data"

    line := FileReadLine(user_include, 1)
    include_key := "#include "
    key_len := StringLen(include_key)
    if SubStr(line, 1, key_len) == include_key
        Return SubStr(line, key_len + 1)

    Return "data"
}

_a2_get_user_config() {
    ; Parse the a2.cfg in the user data dir and equip global a2cfg with values
    a2cfg := {}
    config_path := path_join(a2data, ["a2.cfg"])
    Loop, Read, %config_path%
    {
        parts := StrSplit(A_LoopReadLine, " ",,3)
        varname := Trim(parts[1])
        op := Trim(parts[2])
        value := Trim(parts[3])
        if (op == ":=") {
            if (value == "true")
                a2cfg[varname] := true
            else if (value == "false")
                a2cfg[varname] := false
            else
                a2cfg[varname] := value
        }
    }
    Return a2cfg
}

a2ui_help() {
    Run, %a2_help%
}

a2ui_reload() {
    Reload
}

a2ui_exit() {
    ExitApp
}

a2_explore() {
    Run, %A_WinDir%\explorer.exe %a2dir%
}
