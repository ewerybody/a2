; Things we need for both the un- and installer!
#Include ..\Autohotkey\lib
#Include <string>
#Include <a2dlg>
#Include <path>

/*
Log something to stdout. This would fail on non-console apps like our setup.exe installer
*/
log_msg(msg) {
    try FileAppend(msg . "`n", "*")
}

log_info(title, msg, timeout := 2147483) {
    if check_silent()
        log_msg(title . " " . msg)
    else
        a2dlg_info(msg, title)
}

log_error(title, msg) {
    if check_silent()
        log_msg("ERROR: " . title . " " . msg)
    else
        a2dlg_error(msg, title)
    ExitApp
}

complain_if_uncompiled() {
    If (!A_IsCompiled)
        log_error("Not Compiled!", "'" . A_ScriptName . "'' should ONLY be run compiled!")
}

get_a2dir() {
    ;builds default a2 dir in User\AppData\Local
    ;from roaming but without the dots "..\"
    a2dir := path_join(path_dirname(A_AppData), "Local", "a2")
    return a2dir
}

find_processes_running_under(path) {
    path_len := StrLen(path)
    processes := []

    ; Toolhelp32 snapshot — no subprocess, typically <20 ms
    ; TH32CS_SNAPPROCESS = 0x2
    hSnap := DllCall("CreateToolhelp32Snapshot", "UInt", 0x2, "UInt", 0, "Ptr")
    if (hSnap = -1)
        return processes

    ; PROCESSENTRY32W layout (x64):
    ;   0  DWORD  dwSize
    ;   4  DWORD  cntUsage
    ;   8  DWORD  th32ProcessID
    ;  12  (4-byte pad)
    ;  16  ULONG_PTR th32DefaultHeapID
    ;  24  DWORD  th32ModuleID
    ;  28  DWORD  cntThreads
    ;  32  DWORD  th32ParentProcessID
    ;  36  LONG   pcPriClassBase
    ;  40  DWORD  dwFlags
    ;  44  WCHAR  szExeFile[MAX_PATH]   (520 bytes)
    ;  total = 564, padded to 568
    pe := Buffer(568, 0)
    NumPut("UInt", 568, pe, 0)

    if !DllCall("Process32FirstW", "Ptr", hSnap, "Ptr", pe) {
        DllCall("CloseHandle", "Ptr", hSnap)
        return processes
    }

    loop {
        pid := NumGet(pe, 8, "UInt")
        ; PROCESS_QUERY_LIMITED_INFORMATION = 0x1000 (no admin needed for most processes)
        hProc := DllCall("OpenProcess", "UInt", 0x1000, "Int", 0, "UInt", pid, "Ptr")
        if (hProc) {
            buf  := Buffer(1040, 0)   ; 520 wide chars
            size := Buffer(4)
            NumPut("UInt", 520, size, 0)
            if DllCall("QueryFullProcessImageNameW", "Ptr", hProc,
                    "UInt", 0, "Ptr", buf, "Ptr", size) {
                exe_path := StrGet(buf, "UTF-16")
                if (SubStr(exe_path, 1, path_len) = path) {
                    data := Map()
                    data["ExecutablePath"] := exe_path
                    data["ProcessId"]      := pid
                    data["Name"]           := StrGet(pe.Ptr + 44, 260, "UTF-16")
                    processes.push(data)
                }
            }
            DllCall("CloseHandle", "Ptr", hProc)
        }
        if !DllCall("Process32NextW", "Ptr", hSnap, "Ptr", pe)
            break
    }

    DllCall("CloseHandle", "Ptr", hSnap)
    return processes
}

check_silent() {
    ; look into the commandline arguments for a --silent flag
    for _, arg in A_Args
    {
        if (arg == "--silent")
            Return true
    }
    return false
}

check_execution_dir() {
    dir_name := path_basename(A_ScriptDir)
    parent_dir := path_join(A_ScriptDir, "a2")
    msg := "This could mess things up!`nAborting ..."

    if (dir_name == "_ source") {
        msg := "Running from source dir!? " . msg
        a2dlg_error("Wrong dir?!?!", msg)
    }

    if (!FileExist(parent_dir)) {
        msg := "Not running from 'a2' tmp installation dir!? " . msg
        a2dlg_error("Wrong dir?!?!", msg)
    }
}
