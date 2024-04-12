a2_get_user_data_path(a2dir) {
    ; Get the user data directory from cfg file or:
    ; Set it as "data", right in the the a2 root.
    user_include := "_ user_data_include"
    if !FileExist(user_include) {
        ; Make sure there is a slash at the end:
        return path_join(a2dir, "data", "")
    }

    file_obj := FileOpen(user_include, "r")
    line := file_obj.ReadLine() ;1st
    line := file_obj.ReadLine() ;2nd!
    include_key := "#include "
    key_len := StrLen(include_key)
    if SubStr(line, 1, key_len) == include_key {
        path := string_suffix(SubStr(line, key_len + 1), "\")
        SplitPath path,,,,, &drive_str
        if (!drive_str)
            path := string_suffix(path_join(a2dir, path), "\")

        Return path
    }

    return path_join(a2dir, "data\")
}

a2_get_user_config(a2data) {
    ; Parse the a2.cfg in the user data dir and equip global a2cfg with values
    a2cfg := {}
    config_path := path_join(a2data, "a2.cfg")
    Loop Read, %config_path%
    {
        parts := StrSplit(A_LoopReadLine, " ",,3)
        varname := Trim(parts[1])
        op := Trim(parts[2])
        value := Trim(parts[3])
        _value := StrLower(value)
        if (op == ":=") {
            if (_value == "true")
                a2cfg[varname] := true
            else if (_value == "false")
                a2cfg[varname] := false
            else
                a2cfg[varname] := string_unquote(value)
        }
    }
    Return a2cfg
}