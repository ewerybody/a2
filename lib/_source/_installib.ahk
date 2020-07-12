; Things we need for both the un- and installer!
#Include ..\Autohotkey\lib\string.ahk


complain_if_uncompiled() {
    If (!A_IsCompiled)
    {
        MsgBox, 16, ERROR, "%A_ScriptName%" should ONLY be run compiled!
        ExitApp
    }
}


get_a2dir() {
    ;builds default a2 dir in User\AppData\Local
    ;from roaming but without the dots "..\"
    SplitPath, A_AppData ,, OutDir
    a2dir := OutDir "\Local\a2"
    return a2dir
}


find_processes_running_under(path) {
    attr_list := ["ExecutablePath", "ProcessId", "CommandLine", "Name"]
    attr_ex_path := attr_list[1]
    attrs := string_join(attr_list)
    path_len := StrLen(path)

    ; command =  where name='Autohotkey.exe' get %attrs% /format:list
    command =  get %attrs% /format:list
    result := _find_processes_get_wmic_output(command)

    processes := []
    for i, block in _find_processes_get_blocks(result)
    {
        data := _find_processes_get_key_values(block)
        if !data[attr_ex_path]
            continue
        sub_path := SubStr(data[attr_ex_path], 1, path_len)
        if sub_path = %path%
            processes.push(data)
    }
    return processes
}

_find_processes_get_wmic_output(args) {
    cmd = wmic process %args%
    shell := ComObjCreate("WScript.Shell")
    exec := shell.Exec(ComSpec " /C " cmd)
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
