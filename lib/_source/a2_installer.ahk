; This is the a2 install script added to the 7z package
; compiled to setup.exe. What does it do?
; * get some default paths.
; * compare the install package and probable installed version
; * check for currently running a2 processes
; * backup an installed version
; * install to a2 dir
; * run a2 ui
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico
;@Ahk2Exe-SetVersion 0.5.3

complain_if_uncompiled()
check_execution_dir()

A2DIR := get_a2dir()
A2STUFF := ["lib", "ui", "a2.exe", "a2ui.exe"]
install_ver := read_version(A2DIR)
backup_dir_name := "_ a2 upgrade.bak"
run_silent := check_silent()
PACKAGE_DIR := A_ScriptDir . "\a2"

intro()
check_running()
backup()
install()

Run, a2.exe, %A2DIR%

; --------------------------------------------------------
Return
#Include, _installib.ahk
#include, %A_ScriptDir%\..\Autohotkey\lib
#Include, jxon.ahk

intro() {
    global install_ver, run_silent, PACKAGE_DIR

    new_version := read_version(PACKAGE_DIR)
    title = a2 - %new_version% Installation
    install_msg := "This will install a2 version " . new_version . " for user " . A_UserName . ".`n"
    continue_msg := "`nDo you want to continue? "

    if !has_a2_stuff()
    {
        if (!run_silent) {
            MsgBox, 33, %title%, %install_msg%%continue_msg%
            IfMsgBox Cancel
            {
                ExitApp
            }
        } else {
            logmsg(install_msg)
        }
    } else {
        if install_ver {
            if (install_ver == new_version)
                about_current = Such a version is already installed`n
            else
                about_current = There is currently version "%install_ver%" installed`n
        } else
        about_current = There is currently some version installed`n
        about_current .= "it would be replaced.`n"

        if (!run_silent) {
            MsgBox, 33, %title%, %install_msg%%about_current%%continue_msg%
            IfMsgBox Cancel
            {
                ExitApp
            }
        } else {
            logmsg(install_msg . about_current)
        }
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
    for i, thing in A2STUFF {
        If FileExist(A2DIR "\" thing)
            return 1
    }
    return 0
}

backup() {
    global A2DIR, install_ver, backup_dir_name
    if (!install_ver)
        install_ver := A_Now

    backup_items := []
    Loop, Files, %A2DIR%\*, D
    {
        If (A_LoopFileName == "data")
            continue
        backup_items.Push(A_LoopFileName)
    }
    Loop, Files, %A2DIR%\*, F
    {
        if (A_LoopFileName == "_ user_data_include")
            continue
        backup_items.Push(A_LoopFileName)
    }

    if (!backup_items.Length()) {
        logmsg("Nothing to backup!")
        Return
    }

    delete_later := false
    backup_dir = %A2DIR%\data\temp\%backup_dir_name%\%install_ver%
    logmsg("backing up '" . install_ver . "': " . backup_dir)
    if FileExist(backup_dir) {
        backup_dir = %A_Temp%\%backup_dir_name%\%A_Now%
        logmsg(" version already backed up!: moving to temp:" . backup_dir)
        delete_later := true
    }

    FileCreateDir, %backup_dir%
    for i, item in backup_items {
        this_path := path_join(A2DIR, item)
        back_path := path_join(backup_dir, item)
        if path_is_dir(this_path) {
            logmsg(" backing up dir: " . item)
            FileMoveDir, %this_path%, %back_path%
        } else if path_is_file(this_path) {
            logmsg(" backing up file: '" . item)
            FileMove, %this_path%, %back_path%
        }
    }

    ; In case the version was already backed up, remove the temp backup.
    if delete_later
        FileRemoveDir, %backup_dir%
    else
        remove_if_empty(backup_dir)
}

install() {
    global A2DIR, PACKAGE_DIR
    if (!PACKAGE_DIR)
        log_error("Package dir empty?!", "The package dir should not be '" . PACKAGE_DIR . "'!")
    if (!FileExist(PACKAGE_DIR))
        log_error("Package dir missing?!", "The package dir must exist!`n'" . PACKAGE_DIR . "'!!?")

    Loop, Files, %PACKAGE_DIR%\*, D
        FileMoveDir, %A_LoopFilePath%, %A2DIR%\%A_LoopFileName%
    Loop, Files, %PACKAGE_DIR%\*, F
        FileMove, %A_LoopFilePath%, %A2DIR%\%A_LoopFileName%

    ; make sure the SQLlite-dll can be found
    sqldll := "SQLite3.dll"
    dll_path := path_join(A2DIR, "ui", sqldll)
    if (!FileExist(dll_path))
        log_error(sqldll " missing?!", "The """ sqldll " "" must exist here:`n" dll_path "`n!`nWhere is it?")
    ini_path := path_join(A2DIR, "lib", "SQLiteDB.ini")
    ini_code := "[Main]`nDllPath=" dll_path
    FileAppend, %ini_code%, %ini_path%

    ; If there is no db-file yet, make sure there is an empty one.
    data_path := path_join(A2DIR, "data")
    if (!FileExist(data_path))
        FileCreateDir, %data_path%
    db_path := path_join(data_path, "a2.db")
    if (!FileExist(db_path)) {
        txt := ""
        FileAppend, %txt%, %db_path%
    }
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
    global A2DIR, run_silent
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

        if (run_silent) {
            logmsg("a2 Applications running!" . msg)
            Sleep, 1000
        } else {
            MsgBox 49, a2 Applications running ..., %msg%
            IfMsgBox Cancel
            {
                ExitApp
            }
        }

        for i, proc in processes
        {
            pid := proc.ProcessId
            Process, Close, %pid%
        }
        runs_a2runtime := check_running()
    }

    return runs_a2runtime
}
