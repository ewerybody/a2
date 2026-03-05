/************************************************************************
 * Establish user data path.
 * * If there is a portable entry point file: We're portable!
 * * If there is a custom path file in {LOCALAPPDATA}\\a2\\data
 *   * read the file, return path
 * * Otherwise its {LOCALAPPDATA}\\a2\\data
 * @param {String} a2dir - a2 root app directory string path.
 * @returns {String} Path to the user data.
 ***********************************************************************/
a2_get_user_data_path(a2dir) {
    ENTRYPOINT_FILENAME := 'a2_entry.ahk'
    portable_data := path_join(a2dir, "data")
    portable_entry := path_join(portable_data, ENTRYPOINT_FILENAME)
    if FileExist(portable_entry)
        return portable_data

    CUSTOM_DATA_FILENAME := 'a2_user_data.pth'
    local_data := path_join(EnvGet('LocalAppData'), "a2", "data")
    custom_path_cfg := path_join(local_data, CUSTOM_DATA_FILENAME)
    if !FileExist(custom_path_cfg)
        return local_data

    custom_path := FileRead(custom_path_cfg)
    if DirExist(custom_path)
        return custom_path
    return local_data
}


/**
 * Parse the a2.cfg in the user data dir and equip global a2cfg with values.
 * @param {String} a2data
 * @returns {Map}
 */
a2_get_user_config(a2data) {
    a2cfg := Map()
    config_path := path_join(a2data, "a2.cfg")
    Loop Read, config_path
    {
        parts := StrSplit(A_LoopReadLine, " ",,3)
        var_name := Trim(parts[1])
        op := Trim(parts[2])
        value := Trim(parts[3])
        _value := StrLower(value)
        if (op == ":=") {
            if (_value == "true")
                a2cfg[var_name] := true
            else if (_value == "false")
                a2cfg[var_name] := false
            else
                a2cfg[var_name] := string_unquote(value)
        }
    }
    Return a2cfg
}
