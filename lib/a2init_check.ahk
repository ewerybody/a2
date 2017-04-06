; these init checks are for the root executable scripts

_init_check_settings() {
    ; looks for the essential settings files to be there.
    ; writes those with basic settings if not.
    a2_settings = a2_settings.ahk
    a2_init = a2_init.ahk
    settings_created := false

    settings_dir = %A_ScriptDir%\settings
    ifNotExist, %settings_dir%\%a2_settings%
    {
        IfNotExist, %settings_dir%
            FileCreateDir, %settings_dir%

        FileCopy, lib\_defaults\%a2_settings%, %settings_dir%\%a2_settings%

        ifNotExist, %settings_dir%\libs.ahk
            FileCopy, lib\_defaults\libs.ahk, %settings_dir%\libs.ahk

        modules_dir = %A_ScriptDir%\modules
        IfNotExist, %modules_dir%
            FileCreateDir, %modules_dir%

        includes := ["hotkeys", "variables", "includes", "init"]
        for i, filename in includes
        {
            msg := "; a2 " filename ".ahk - Don't bother editing! - File is generated automatically!`n"
            FileAppend, %msg%, %A_ScriptDir%\settings\%filename%.ahk
        }

        a2db_path = %settings_dir%\a2.db
        ifNotExist, %a2db_path%
            FileAppend, , %a2db_path%
        
        settings_created := true
    }
    IfNotExist, %settings_dir%\%a2_init%
        FileCopy, lib\_defaults\%a2_init%, %settings_dir%\%a2_init%

    Return settings_created
}

_init_get_var(var_name, relative="\..") {
    ; reads a2_settings.ahk and returns the value of a given variable name.
    ; without including the file
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
    ; reads the a2_settings.ahk
    ; returns given Autohotkey.exe if found
    ; returns default Autohotkey.exe in lib if not
    ahk_exe := _init_get_var("a2_ahk", "")
    ifNotExist, %ahk_exe%
        ahk_exe = %A_ScriptDir%\lib\Autohotkey\Autohotkey.exe
    Return ahk_exe
}
