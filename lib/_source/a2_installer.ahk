; This is the a2 install script added to the 7z package
; compiled to setup.exe. What does it do?
; * get some default paths.
; * compare the install package and probable installed version
; * check for currently running a2 processes
; * backup an installed version
; * install to a2 dir
; * run a2 ui

complain_if_uncompiled()

A2DIR := get_a2dir()
A2STUFF := ["lib", "ui", "a2.exe", "a2ui.exe"]
install_ver := read_version(A2DIR)
backup_dir_name := "_ a2 upgrade.bak"
install_script := "setup.exe"

intro()
runs_a2runtime := check_running()
backup_dir := backup()
install(backup_dir)

Run, %A2DIR%\a2ui.exe

; --------------------------------------------------------
Return
#include ..\Autohotkey\lib\jxon.ahk
#Include, _installib.ahk

intro() {
    global install_ver
    new_version := read_version(A_ScriptDir)
    title = a2 - %new_version% Installation
    install_msg = This will install a2 version "%new_version%" for user "%A_UserName%".`n
    continue_msg := "`nDo you want to continue?"
    if !has_a2_stuff()
    {
        MsgBox, 33, %title%, %install_msg%%continue_msg%
        IfMsgBox Cancel
            ExitApp
    } else {
        if install_ver {
            if (install_ver == new_version)
                about_current = Such a version is already installed`n
            else
                about_current = There is currently version "%install_ver%" installed`n
        } else
            about_current = There is currently some version installed`n
        about_current .= "it would be replaced.`n"

        MsgBox, 33, %title%, %install_msg%%about_current%%continue_msg%
        IfMsgBox Cancel
            ExitApp
    }
}

read_version(path) {
    package_path = %path%\package.json
    if FileExist(package_path)
    {
        data := jxon_read(package_path)
        v := data["version"]
        return %v%
    }
    else
        return ""
}

has_a2_stuff() {
    global A2STUFF, A2DIR
    for i, thing in A2STUFF
        If FileExist(A2DIR "\" thing)
            return 1
    return 0
}

backup() {
    global A2DIR, install_ver, backup_dir_name
    if (!install_ver)
        install_ver := A_Now

    delete_later := false
    backup_dir = %A2DIR%\data\temp\%backup_dir_name%\%install_ver%
    IfExist, %backup_dir%
    {
        delete_later := true
        backup_dir = %A_Temp%\%backup_dir_name%\%A_Now%
    }

    FileCreateDir, %backup_dir%
    Loop, Files, %A2DIR%\*, D
    {
        If (A_LoopFileName == "data")
            continue
        FileMoveDir, %A_LoopFilePath%, %backup_dir%\%A_LoopFileName%
    }
    Loop, Files, %A2DIR%\*, F
        FileMove, %A_LoopFilePath%, %backup_dir%\%A_LoopFileName%

    if delete_later
        FileRemoveDir, %backup_dir%
    else
        remove_if_empty(backup_dir)

    return backup_dir
}

install(backup_dir) {
    global A2DIR, install_script
    Loop, Files, %A_ScriptDir%\*, D
        FileMoveDir, %A_LoopFilePath%, %A2DIR%\%A_LoopFileName%
    Loop, Files, %A_ScriptDir%\*, F
    {
        If (A_LoopFileName == install_script)
            continue
        FileMove, %A_LoopFilePath%, %A2DIR%\%A_LoopFileName%
    }

    ;recover _ user include file
    rel_path = \_ user_data_include.cfg
    IfExist, %backup_dir%%rel_path%
        FileCopy, %backup_dir%%rel_path%, %A2DIR%%rel_path%
}

remove_if_empty(path) {
    global backup_dir_name
    if !_remove_if_empty(path)
        return

    SplitPath, path ,, OutDir
    SplitPath, OutDir , OutFileName
    if (OutFileName == backup_dir_name)
        _remove_if_empty(OutDir)
}

_remove_if_empty(path) {
    empty := true
    Loop, Files, %path%\*, FD
    {
        empty := false
        return empty
    }
    if empty
        FileRemoveDir, %path%
    return empty
}


check_running() {
    global A2DIR
    processes := find_processes_running_under(A2DIR)
    runs_a2runtime := false
    names := []
    for i, proc in processes
    {
        names.push(proc.name)
        if (proc.name = "Autohotkey.exe" && string_endswith(proc.CommandLine, " lib\a2.ahk"))
            runs_a2runtime := true
    }
    if (names.length()) {
        name_string := string_join(names)
        msg := "Some a2 applications are currently running!`n"
        msg .= "To savely continue the installation I'd suggest to shutdown these processes ("
        msg .= name_string . ").`n`n"
        msg .= "Or you hit Cancel, do it by yourself and start the installation again."

        MsgBox 49, a2 Applications running ..., %msg%
        IfMsgBox Cancel
            ExitApp

        for i, proc in processes
        {
            pid := proc.ProcessId
            Process, Close, %pid%
        }
        check_running()
    }

    return runs_a2runtime
}
