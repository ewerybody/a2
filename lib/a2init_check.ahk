; these init checks are for the root executable scripts

_init_get_var(var_name, relative="\..") {
    ; reads a2_settings.ahk and returns the value of a given variable name.
    ; without including the file
    default_config = %A_ScriptDir%%relative%\lib\a2_config.ahk
    user_config = 
    settings_dir = %A_ScriptDir%%relative%\settings
    Loop, read, %settings_dir%\a2_settings.ahk
    {
        parts := StrSplit(A_LoopReadLine, ["=", ":="])
        this_name := Trim(parts[1])

        if (this_name == var_name) {
            value := Trim(parts[2])
            Return value
        }
    }
}


_init_get_autohotkey_exe() {
    ; returns default Autohotkey.exe in lib
    ahk_exe = %A_ScriptDir%\lib\Autohotkey\Autohotkey.exe
    Return ahk_exe
}
