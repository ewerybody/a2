; a2 - modular Autohotkey script envirionment
; main file! This gathers all the runtime resources
#SingleInstance force
Persistent
; #NoTrayIcon

#include <Class_SQLiteDB>
#include <path>
#include <string>
#include <msgbox>
#include <cursor>
#include <a2tip>
#include <a2log>
#include <explorer>

#include a2_core.ahk
#include a2_config.ahk
#include a2_globals.ahk
#include a2_urls.ahk
#include a2_exceptions.ahk
#include a2_user_data.ahk

; build essential paths and objects
root_dir := path_dirname(A_ScriptDir) "\"
data_dir := a2_get_user_data_path(root_dir)
global a2 := A2Core_Class(data_dir)
a2.cfg := a2_get_user_config(data_dir)
SetWorkingDir a2.paths.a2

_a2_check_arguments()
_a2_build_tray_menu(a2_title)

if !a2.cfg.get("no_startup_tooltip", 0)
    a2tip(a2_title)

if a2.cfg.get("auto_reload", 1)
    SetTimer _a2_check_changes, 1000

OnExit(a2ui_exit)
; OnError("a2_on_runtime_exception")

; Snippet from: https://github.com/kdalanon/ChatGPT-AutoHotkey-Utility
; Class DarkMode {
;     Static __New(Mode := 1) => ( ; Mode: Dark = 1, Default (Light) = 0
;         DllCall(DllCall("GetProcAddress", "ptr", DllCall("GetModuleHandle", "str", "uxtheme", "ptr"), "ptr", 135, "ptr"), "int", mode),
;         DllCall(DllCall("GetProcAddress", "ptr", DllCall("GetModuleHandle", "str", "uxtheme", "ptr"), "ptr", 136, "ptr"))
;     )
; }

; Finally the user data includes. Happening in the end
; so the top of this main script is executed before first Return.
#include *i "_ user_data_include"
Return ; -----------------------------------------------------------------------

a2ui(*) {
    tt_text := "Calling a2 ui ..."
    a2tip(tt_text)
    a2_win_id := WinExist("a2 ahk_class Qt623QWindowIcon ahk_exe pythonw.exe")
    if (a2_win_id)
        WinActivate "ahk_id " a2_win_id
    else {
        ui_starter := path_join(a2.paths.a2, "a2ui.exe")
        Run ui_starter
    }
}

a2ui_help(*) {
    Run a2_help
}

a2ui_reload(*) {
    Reload
}

a2ui_exit(*) {
    exit_func := "a2_exit_calls"
    if IsObject(exit_func)
        %exit_func%()
    ExitApp
}

a2_explore(*) {
    ; Open the a2 root directory in the file browser.
    explorer_show(a2.paths.a2)
}

_a2_check_changes() {
    ; Check library & module scripts for changes via archive file attribute.
    ; Removes the attribute from all files and returns true if any was found
    do_reload := false
    for _, libdir in [a2.paths.lib, a2.paths.ahklib] {
        Loop Files, string_suffix(libdir, "\") "*.ahk"
        {
            If InStr(A_LoopFileAttrib, "A") {
                do_reload := true
                FileSetAttrib "-A", A_LoopFileFullpath
                a2log_debug("Changed lib file: " A_LoopFileFullPath)
            }
        }
    }

    Loop read a2.paths.includes
    {
        if !string_startswith(A_LoopReadLine, "#include ")
            Continue

        path := path_join(a2.paths.data, SubStr(A_LoopReadLine, 10))
        if InStr(FileGetAttrib(path), "A") {
            do_reload := true
            a2log_debug("Changed include file: " path)
            FileSetAttrib "-A", path
        }
    }

    if (do_reload) {
        a2ui_reload()
    }
}

_a2_check_arguments() {
    ; Look into the commandline arguments for certain flags.
    for _, arg in A_Args {
        if (arg == "--shutdown")
            ExitApp
        else
            MsgBox("Arguments handling is WIP!`nWhat's '" arg "'?", "a2")
    }
}

_a2_build_tray_menu(a2_title) {
    ; Build the tray icon menu.
    a2ui_res := a2.paths.resources
    TraySetIcon(path_join(a2.paths.resources, "a2.ico"))
    A_TrayMenu.Delete()

    A_TrayMenu.Add("Open a2 User Interface", a2ui)
    A_TrayMenu.SetIcon("Open a2 User Interface", a2ui_res "a2.ico")
    A_TrayMenu.Add("Open a2 Directory", a2_explore)
    A_TrayMenu.SetIcon("Open a2 Directory", a2ui_res "a2.ico")
    A_TrayMenu.Add("Reload a2 Runtime", a2ui_reload)
    A_TrayMenu.SetIcon("Reload a2 Runtime", a2ui_res "a2reload.ico")
    A_TrayMenu.Add("Help on a2", a2ui_help)
    A_TrayMenu.SetIcon("Help on a2", a2ui_res "a2help.ico")
    A_TrayMenu.Add("Quit a2 Runtime", a2ui_exit)
    A_TrayMenu.SetIcon("Quit a2 Runtime", a2ui_res "a2x.ico")

    A_IconTip := a2_title
    A_TrayMenu.ClickCount := 1
    A_TrayMenu.Default := "Open a2 User Interface"
}
