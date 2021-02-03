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

_a2_check_arguments()
_a2_build_tray_menu(a2_title)

global a2cfg := _a2_get_user_config()

if !a2cfg.no_startup_tooltip
    tt(a2_title, 1)

if a2cfg.auto_reload
    SetTimer, _a2_check_changes, 1000

OnExit("a2ui_exit")
OnError("_a2ui_on_error")

; Finally the user data includes. Happening in the end
; so the top of this main script is executed before first Return.
#include *i _ user_data_include
Return ; -----------------------------------------------------------------------

a2ui() {
    tt_text := "Calling a2 ui ..."
    tt(tt_text)
    a2_win_id := WinExist("a2 ahk_class Qt5152QWindowIcon ahk_exe pythonw.exe")
    if (a2_win_id)
        WinActivate, ahk_id %a2_win_id%
    else {
        a2_ahk := A_ScriptDir "\Autohotkey\Autohotkey.exe"
        Run, "%a2_ahk%" "%A_ScriptDir%\a2ui.ahk", %A_ScriptDir%
        WinWait, a2,, 5
    }
    tt(tt_text, 1)
}

a2ui_help() {
    Run, %a2_help%
}

a2ui_reload() {
    Reload
}

a2ui_exit() {
    exit_func := "a2_exit_calls"
    if IsFunc(exit_func)
        %exit_func%()
    ExitApp
}
_a2ui_exit() {
    ExitApp
}

a2_explore() {
    ; Open the a2 root directory in the file browser.
    Run, %A_WinDir%\explorer.exe %a2dir%
}

_a2_check_changes() {
    ; Check library & module scripts for changes via archive file attribute.
    ; Removes the attribute from all files and returns true if any was found
    do_reload := false
    for _, libdir in [a2lib, path_join(a2lib, ["Autohotkey", "lib"])] {
        pattern := string_suffix(libdir, "\") "*.ahk"
        Loop, Files, %pattern%
        {
            If InStr(A_LoopFileAttrib, "A") {
                do_reload := true
                FileSetAttrib, -A, %A_LoopFileFullpath%
            }
        }
    }

    includes_path := path_join(a2data, ["includes", "includes.ahk"])
    Loop, read, %includes_path%
    {
        if !string_startswith(A_LoopReadLine, "#include ")
            Continue

        path := path_join(a2data, [SubStr(A_LoopReadLine, 10)])
        if InStr(FileGetAttrib(path), "A") {
            do_reload := true
            FileSetAttrib, -A, %path%
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
        return path_join(a2dir, ["data\"])

    line := FileReadLine(user_include, 2)
    include_key := "#include "
    key_len := StringLen(include_key)
    if SubStr(line, 1, key_len) == include_key {
        path := string_suffix(SubStr(line, key_len + 1), "\")
        SplitPath, path,,,,, drive_str
        if (!drive_str)
            path := string_suffix(path_join(a2dir, [path]), "\")

        Return path
    }

    return path_join(a2dir, ["data\"])
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
        _value := StringLower(value)
        if (op == ":=") {
            if (_value == "true")
                a2cfg[varname] := true
            else if (_value == "false")
                a2cfg[varname] := false
            else
                a2cfg[varname] := value
        }
    }
    Return a2cfg
}

_a2_check_arguments() {
    ; Look into the commandline arguments for certain flags.
    for _, arg in A_Args {
        if (arg == "--shutdown")
            ExitApp
        else
            MsgBox, a2, Arguments handling is WIP!`nWhat's "%arg%"?
    }
}

_a2ui_on_error(exception) {
    file_path := exception.File, line_nr := exception.Line
    FileReadLine, code_line, %file_path%, %line_nr%
    file_name := path_basename(file_path)

    msg := "There was an exception thrown:`n " exception.Message "`n"
    msg .= "command: """ exception.What """`n"
    msg .= "value: """ exception.Extra """`n"
    msg .= "file: " file_name ", Line: " line_nr "`n"
    msg .= ">>>" code_line
    title := "a2 Runtime Error: " exception.Message

    SetTimer, _a2ui_on_error_change_buttons, 50
    MsgBox, 19, %title%, %msg%
    IfMsgBox, Yes
    {
        editor := "C:\Users\eric\AppData\Local\Programs\Microsoft VS Code Insiders\Code - Insiders.exe"
        file_line := exception.File ":" exception.Line
        Run, "%editor%" --reuse-window --goto "%file_line%"
    }
    IfMsgBox, No
    a2ui()

    Reload

    _a2ui_on_error_change_buttons:
        IfWinNotExist, %title%
            return ; Keep waiting.
        SetTimer, _a2ui_on_error_change_buttons, Off
        WinActivate
        ControlSetText, Button1, Edit Code
        ControlSetText, Button2, Open UI
    Return
}

_a2_build_tray_menu(a2_title) {
    ; Build the tray icon menu.
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
    Menu, Tray, add, Quit a2 Runtime, _a2ui_exit
    Menu, Tray, icon, Quit a2 Runtime, %a2ui_res%a2x.ico
}
