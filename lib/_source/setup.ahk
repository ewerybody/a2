#Include ..\Autohotkey\lib\string.ahk
#include ..\Autohotkey\lib\jxon.ahk

If (!A_IsCompiled)
{
    MsgBox, 16, ERROR, This should ONLY be run compiled!
    ExitApp
}

A2DIR := get_a2dir()
A2STUFF := ["lib", "ui", "a2.exe", "a2ui.exe"]
install_ver := read_version(A2DIR)
backup_dir_name := "_ a2 upgrade.bak"
install_script := "setup.exe"

intro()
runs_a2runtime := check_running()
backup_dir := backup()
install(backup_dir)
if runs_a2runtime
    Run, %A2DIR%\a2.exe, %A2DIR%

; --------------------------------------------------------
Return

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
    IfExist, %package_path%
    {
        FileRead, content, %package_path%
        data := jxon_load(content)
        v := data["version"]
        return %v%
    }
    else
        return ""
}

has_a2_stuff() {
    global A2STUFF, A2DIR
    for i, thing in A2STUFF
        IfExist, %A2DIR%\%thing%
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
    rel_path = \lib\_ user_data_includes.ahk
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
        MsgBox 49, a2 Applications running ..., Some a2 applications are currently running!`nTo savely continue the installation I'd suggest to shutdown these processes (%name_string%).`n`nOr you hit Cancel, do it by yourself and start the installation again.
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

find_processes_running_under(path) {
    attr_list := ["ExecutablePath", "ProcessId", "CommandLine", "Name"]
    attr_ex_path := attr_list[1]
    attrs := string_join(attr_list)
    path_len := StrLen(path)

    ; command =  where name='Autohotkey.exe' get %attrs% /format:list
    command =  get %attrs% /format:list
    result := get_wmic_process_output(command)
    
    processes := []
    for i, block in get_blocks(result)
    {
        data := get_key_values(block)
        if !data[attr_ex_path]
            continue
        sub_path := SubStr(data[attr_ex_path], 1, path_len)
        if sub_path = %path%
            processes.push(data)
    }
    return processes
}

get_a2dir() {
    ;builds default a2 dir in User\AppData\Local
    ;from roaming but without the dots "..\"
    SplitPath, A_AppData ,, OutDir
    a2dir = %OutDir%\Local\a2
    return a2dir
}

get_wmic_process_output(args) {
    cmd = wmic process %args%
    shell := ComObjCreate("WScript.Shell")
    exec := shell.Exec(ComSpec " /C " cmd)
    result := exec.StdOut.ReadAll()
    return result
}

get_blocks(string) {
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

get_key_values(string_block) {
    lines := StrSplit(string_block, "`r`r`n")
    results := {}
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
