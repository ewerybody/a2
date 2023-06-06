; a2 uninstaller
; * remove Desktop link
; * remove autostart link
; * remove Start Menu links
; * shut down running a2 processes
; * ask user for user data deletion
; * delete things in a2 data dir
; * write uninstall deleter batch file
; * run uninstall deleter batch
; * exit
;@Ahk2Exe-ConsoleApp
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2x.ico
;@Ahk2Exe-SetCompanyName a2
;@Ahk2Exe-SetCopyright GPLv3
;@Ahk2Exe-SetDescription a2 Uninstaller
;@Ahk2Exe-SetOrigFilename Uninstall a2.exe
;@Ahk2Exe-SetProductName a2
;@Ahk2Exe-SetVersion 0.5.4


complain_if_uncompiled()

run_silent := check_silent()
A2DIR := get_a2dir()
NAME := "a2 Uninstaller"

items := gather_items()
outro(items)
ask_for_user_data_deletion(items)
delete_items(items)

batch_path := create_deleter_batch(A2DIR)
logmsg(" calling installer deleter...")
Run, %batch_path%,,Min
ExitApp

; --------------------------------------------------------
Return
#Include, _installib.ahk

outro(items) {
    global run_silent, NAME

    if (!items.Length()) {
        msg := "There is nothing to Uninstall!"
        log_info(NAME, msg)
        ExitApp
    }

    processes := check_processes()
    if (processes.Length()) {
        process_msg := "There are still processes running from the installation ("
        process_msg .= processes.Length() . ").`n"
        process_msg .= "Either you shut them down yourself or they'd be terminated.`n"
    }
    uninstall_msg := "This will Uninstall a2 for user """ . A_UserName . """.`n"
    continue_msg := "`nDo you want to continue?"
    if (!run_silent) {
        MsgBox, 33, %NAME%, %uninstall_msg%%process_msg%%continue_msg%
        IfMsgBox, Cancel
        {
            ExitApp
        }
    } else {
        logmsg(uninstall_msg)
    }

    ; shut down processes
    for i, proc in processes {
        logmsg(" closing process: " . proc.ProcessId . "...")
        Process, Close, % proc.ProcessId
    }
}

gather_items() {
    global A2DIR
    items := []
    if FileExist(A2DIR) {
        Loop, Files, %A2DIR%\*.*, FD
        {
            ; Skip Uninstaller executable for now (cannot delete itself while running)
            if (A_LoopFileName == A_ScriptName)
                continue
            ; do not touch the users data include file
            if (A_LoopFileName == "_ user_data_include")
                continue
            ; Skip the user data, add it only on demand.
            if (A_LoopFileName == "data" AND path_is_dir(A_LoopFileFullPath))
                continue
            items.push(A_LoopFileFullPath)
        }
    }

    ; collect Desktop link if it goes to A2DIR
    desktop_link_path := A_Desktop "\a2ui.lnk"
    FileGetShortcut, %desktop_link_path%, desktop_link_target
    default_path := A2DIR "\a2ui.exe"
    if (desktop_link_target == default_path)
        items.push(desktop_link_path)

    ; collect Startup link if it goes to A2DIR
    startup_link_path := A_Startup "\a2.lnk"
    FileGetShortcut, %startup_link_path%, startup_link_target
    default_path := A2DIR "\a2.exe"
    if (startup_link_target == default_path)
        items.push(startup_link_path)

    ; collect Start Menu links if they go to A2DIR
    start_menu_dir := A_Programs "\a2"
    if FileExist(start_menu_dir) {
        links_found := false
        Loop, Files, %start_menu_dir%\*.lnk
        {
            FileGetShortcut, %A_LoopFileFullPath%, this_link_target
            if string_startswith(this_link_target, A2DIR)
            {
                links_found := true
                items.push(A_LoopFileFullPath)
            }
        }

        if links_found
            items.push(start_menu_dir)
    }

    return items
}

ask_for_user_data_deletion(ByRef items) {
    global A2DIR, run_silent
    if run_silent
        return
    user_data_path := path_join(A2DIR, "data")

    if FileExist(user_data_path) {
        MsgBox, 36, Delete User data?, Do you also want to delete the user data?
        IfMsgBox Yes
        {
            items.push(user_data_path)
            items.push("_ user_data_include")
        }
    }
}

delete_items(items) {
    global A2DIR, run_silent

    num_items := items.Length()
    if (!run_silent)
        Progress, r0-%num_items% w500 cb36EC95, ...,, %NAME%, Small Fonts

    for i, path in items {
        if (!run_silent)
            Progress, %i%, %path%

        if path_is_dir(path) {
            logmsg(" deleting dir: " . path)
            FileRemoveDir, %path%, 1
        } else if path_is_file(path) {
            FileDelete, %path%
        }
        Sleep, 50
    }

    if (!run_silent) {
        Progress, %num_items%, Okithxbye!
        Sleep, 500
        Progress, Off
    }

    for i, path in items {
        if FileExist(path)
            log_info(NAME, "Could not delete: " . path)
    }
}

; - Assemble simple windows batch code
create_deleter_batch(path) {
    ;   * cd into Temp dir
    ;   * delete running executable (If compiled)
    ;   * try a couple times
    ;   * delete given path (IF Empty!)
    ;   * delete itself
    ; - Write to Temp
    ; - return file path

    if (!path)
        log_error("create_deleter_batch", "No path given!")

    batch_path := path_join(A_Temp, "_ a2_uninstaller_deleter.bat")
    batch_sleep := "ping 127.0.0.1 -n 1 > nul`n"

    content := "@echo off`n"
    content .= "cd """ . A_Temp . """`n"
    ; wait for the Uninstaller executable to shut down before deleting it
    content .= batch_sleep
    content .= "set trg_dir=" . path . "`n"

    If (A_IsCompiled) {
        if (path_join(path, A_ScriptName) == A_ScriptFullPath)
            content .= "set trg_exe=%trg_dir%\" . A_ScriptName . "`n"
        else
            content .= "set trg_exe=" . A_ScriptFullPath . "`n"
        content .= "for /L %%A IN (1,1,500) do (`n"
        content .= " if not exist ""%trg_exe%"" (goto deleted)`n"
        content .= " DEL ""%trg_exe%"" /f /q > nul 2> nul`n"
        content .= batch_sleep
        content .= ")`n"
    }
    content .= ":deleted`n"
    ; skip deleting the folder if not empty
    content .= "for /F %%i in ('dir /b /a ""%trg_dir%\*""') do (`n"
    ; content .= "  echo Not Empty!`n"
    content .= " goto finalize`n"
    content .= ")`n"
    ; content .= "echo IS Empty!`n"
    content .= batch_sleep
    content .= "RMDIR /Q ""%trg_dir%""`n"
    content .= ":finalize`n"
    content .= batch_sleep
    ; content .= "pause`n"
    content .= "(goto) 2>nul & del ""%~f0"""

    FileDelete %batch_path%
    FileAppend, %content%, %batch_path%
    Return %batch_path%
}

check_processes() {
    global A2DIR
    all_processes := find_processes_running_under(A2DIR)
    resulting_procs := []
    for i, proc in all_processes
        if (proc.ExecutablePath != A_ScriptFullPath)
        resulting_procs.push(proc)
    return resulting_procs
}
