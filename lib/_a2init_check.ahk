; these init checks are for the root executable scripts

_init_get_lib_path() {
    ; To be able to run the starter without compiling
    if string_endswith(A_ScriptDir, "\lib\_source")
        return path_dirname(A_ScriptDir)
    else {
        lib_path := path_join(A_ScriptDir, "lib")
        if path_is_dir(lib_path)
            return lib_path
        else
            msgbox_error("_init_get_lib_path() should either be in _source or in the root and have a lib subdir :/"
                , "Where am I?!?")
    }
}


_init_get_autohotkey_exe() {
    ; returns default Autohotkey.exe in lib
    lib_path := _init_get_lib_path()
    ahk_exe := path_join(lib_path, "Autohotkey", "Autohotkey.exe")
    Return ahk_exe
}
