; a2 - Modular Autohotkey script environment.
; Main file! This gathers all the runtime resources.
#SingleInstance force
Persistent

#include <path>
#include <string>
#include <msgbox>
#include <cursor>
#include <a2tip>
#include <a2log>
#include <python>
#include <explorer>
#include <windows>

#include a2core.ahk
#include a2icon.ahk
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
global A2Icons
SetWorkingDir a2.paths.a2

_a2_check_arguments()
_a2_build_tray_menu(a2_title)

if !a2.cfg.get("no_startup_tooltip", 0)
    a2tip(a2_title)

if a2.cfg.get("auto_reload", 1)
    SetTimer _a2_check_changes, 1000

OnExit(a2ui_exit)
; OnError("a2_on_runtime_exception")


; TODO: make this depending on user-settings!
if windows_is_dark()
    windows_set_theme(mode := 1)


a2ui(*) {
    a2tip("Calling a2 ui ...")
    a2_win_id := WinExist("a2 ahk_class Qt623QWindowIcon ahk_exe pythonw.exe")
    if (a2_win_id) {
        WinActivate "ahk_id " a2_win_id
        return
    }

    show_console := false
    if show_console
        py_exe := path_join(a2.paths.ui, "python.exe")
    else
        py_exe := path_join(a2.paths.ui, "pythonw.exe")

    if !FileExist(py_exe) {
        if show_console
            py_exe := python_get_console_path()
        else
            py_exe := python_get_path()
    }
    if !FileExist(py_exe) {
        msgbox_error("There is no Python runtime to execute the UI with!`n", "a2UI Startup Error")
        Return
    }

    ui_script := path_join(a2.paths.ui, "a2app.py")
    Run('"' py_exe '" "' ui_script '"', a2.paths.ui)
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
    ; Removes the attribute from ALL files and reloads if any was found.
    do_reload := false
    for lib_dir in [a2.paths.lib, a2.paths.ahklib] {
        Loop Files, string_suffix(lib_dir, "\") "*.ahk"
        {
            If InStr(A_LoopFileAttrib, "A") {
                do_reload := true
                FileSetAttrib "-A", A_LoopFileFullpath
                a2log_debug("Changed lib file: " A_LoopFileFullPath)
            }
        }
    }

    if FileExist(a2.paths.includes) {
        Loop read a2.paths.includes {
            if !string_startswith(A_LoopReadLine, "#include ")
                Continue

            path := path_join(a2.paths.data, SubStr(A_LoopReadLine, 10))
            if !FileExist(path)
                Continue
            if InStr(FileGetAttrib(path), "A") {
                do_reload := true
                a2log_debug("Changed include file: " path)
                FileSetAttrib "-A", path
            }
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
