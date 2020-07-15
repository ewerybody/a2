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

complain_if_uncompiled()

A2DIR := get_a2dir()
items := gather_items()
outro(items)

; --------------------------------------------------------
Return
#Include, _installib.ahk
#Include ..\Autohotkey\lib\path.ahk


outro(items) {
    if (!items.Length()) {
        msgbox, 64, a2 Uninstaller, There is nothing to Uninstall!
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
    title := "a2 Uninstaller"
    MsgBox, 33, %title%, %uninstall_msg%%process_msg%%continue_msg%
    IfMsgBox Cancel
        ExitApp

    ; shut down processes
    for i, proc in processes
        Process, Close, % proc.ProcessId

    ask_for_user_data_deletion(items)

    delete_items(items)

    batch_path := create_deleter_batch()
    Run, %batch_path%
    ExitApp
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
    global A2DIR
    del_user_data := false
    for i, path in items {
        if (path == A2DIR "\data") {
            MsgBox, 36, Delete User data?, Do you also want to delete the user data?
            IfMsgBox Yes
                del_user_data := true
            Break
        }
    }
    if (!del_user_data) {
        path_at_i := items[i]
        num_items := items.Length()
        msgbox i: %i%`npath_at_i: %path_at_i%`nnum_items: %num_items%
        items.RemoveAt(i)
        num_items := items.Length()
        msgbox num_items now: %num_items%
    }
}


delete_items(items) {
    global A2DIR

    num_items := items.Length()
    ; Progress, r%num_items%-0 w500 cb37ED95, ..., a2 Uninstaller ...,
    ; Progress, r%num_items%-0 w500, ..., a2 Uninstaller ...,
    Progress, r0-%num_items% w500 cb37ED95, ...,, a2 Uninstaller, Small Fonts
    ; Sleep, 1000

    for i, path in items {
        Progress, %i%, %path%
        if path_is_dir(path) {
            FileRemoveDir, %path%, 1
        } else if path_is_file(path) {
            FileDelete, %path%
        }
        Sleep, 50
    }

    Progress, %num_items%, Okithxbye!
    Sleep, 500
    Progress, Off

    for i, path in items
        if FileExist(path)
            MsgBox Could not delete: %path%
}


create_deleter_batch() {
    ; - Assemble simple windows batch code
    ;   * cd into Temp dir
    ;   * delete uninstaller executable
    ;   * delete the Local\a2 dir (IF Empty!)
    ;   * delete itself
    ; - Write to Temp
    ; - return file path

    global A2DIR
    batch_path := path_join(A_Temp, ["_ a2_uninstaller_deleter.bat"])
    batch_sleep := "ping 127.0.0.1 -n 1 > nul`n"

    content := "@echo off`n"
    content .= "cd """ . A_Temp . """`n"
    ; wait for the Uninstaller executable to shut down before deleting it
    content .= batch_sleep
    If (A_IsCompiled) {
        content .= "DEL """ . A_ScriptFullPath . """`n"
        content .= batch_sleep
    }
    ; skip deleting the folder if not empty
    content .= "for /F %%i in ('dir /b /a """ . A2DIR . "\*""') do (`n"
    ; content .= "  echo Not Empty!`n"
    content .= "  goto finalize`n"
    content .= ")`n"
    ; content .= "echo IS Empty!`n"
    content .= batch_sleep
    content .= "RMDIR /Q """ . A2DIR . """`n"
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
