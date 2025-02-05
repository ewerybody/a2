; Things we need for both the un- and installer!
#Include ..\Autohotkey\lib
#Include <string>
#Include <msgbox>
#Include <path>

/*
Log something to stdout. This would fail on non-console apps like our setup.exe installer
*/
logmsg(msg) {
    try FileAppend(msg . "`n", "*")
}

log_info(title, msg, timeout := 2147483) {
    if check_silent()
        logmsg(title . " " . msg)
    else
        msgbox_info(msg, title)
}

log_error(title, msg) {
    if check_silent()
        logmsg("ERROR: " . title . " " . msg)
    else
        msgbox_error(msg, title)
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
    attr_list := ["ExecutablePath", "ProcessId", "CommandLine", "Name"]
    attr_ex_path := attr_list[1]
    path_len := StrLen(path)

    ; command =  where name='Autohotkey.exe' get %attrs% /format:list
    command := "get " . string_join(attr_list) . " /format:list"
    result := _find_processes_get_wmic_output(command)

    processes := []
    for i, block in _find_processes_get_blocks(result)
    {
        data := _find_processes_get_key_values(block)
        if !data[attr_ex_path]
            continue
        sub_path := SubStr(data[attr_ex_path], 1, path_len)
        if sub_path = path
            processes.push(data)
    }
    return processes
}

_find_processes_get_wmic_output(args) {
    cmd := "wmic process " . args
    shell := ComObject("WScript.Shell")
    exec := shell.Exec(A_ComSpec " /C " cmd)
    result := exec.StdOut.ReadAll()
    return result
}

_find_processes_get_blocks(string) {
    blocks := StrSplit(string, "`r`r`n`r`r`n")
    results := []
    for i, block in blocks
    {
        block := Trim(block, " `n`r")
        if !block
            continue
        results.push(block)
    }
    return results
}

_find_processes_get_key_values(string_block) {
    lines := StrSplit(string_block, "`r`r`n")
    results := Map()
    for i, line in lines
    {
        line := Trim(line, " `n`r")
        if !line
            continue
        cut_pos := InStr(line, "=") + 1
        key := SubStr(line, 1, cut_pos - 2)
        value := SubStr(line, cut_pos)
        results[key] := value
    }
    return results
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
        log_error("Wrong dir?!?!", msg)
    }

    if (!FileExist(parent_dir)) {
        msg := "Not running from 'a2' tmp installation dir!? " . msg
        log_error("Wrong dir?!?!", msg)
    }
}
