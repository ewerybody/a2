; This is the script that becomes the a2.exe in root!
; Overhauled for ahk2 there were some things removed.
; TBD: Look into re-implementation
; * cursor reset?
; * check_load_time_errors - there are fare better error dialogs in ahk2,
;   we might not need anything better?
;@Ahk2Exe-SetMainIcon ..\..\ui\res\a2.ico
;@Ahk2Exe-SetCompanyName a2
;@Ahk2Exe-SetCopyright GPLv3
;@Ahk2Exe-SetDescription a2 runtime starter
;@Ahk2Exe-SetOrigFilename a2.exe
;@Ahk2Exe-SetProductName a2
;@Ahk2Exe-SetVersion 0.6.0
;@Ahk2Exe-Base ..\..\Autohotkey\AutoHotkey.exe

#include ..\Autohotkey\lib\path.ahk
#include ..\a2_globals.ahk
#include ..\Autohotkey\lib\string.ahk
#include ..\Autohotkey\lib\msgbox.ahk
; #include ..\_a2init_check.ahk
; #include ..\a2_core.ahk
; #include ..\a2_exceptions.ahk
; #include ..\a2_user_data.ahk


If (!A_IsCompiled) {
    msgbox_error("a2_starter should ONLY be run compiled!")
    ExitApp
}

lib_path := _init_get_lib_path()
a2_ahk := path_join(lib_path, "Autohotkey", "Autohotkey.exe")
root_path := path_dirname(lib_path)
; a2data := a2_get_user_data_path(root_path)
; global a2 := A2Core_Class(a2data)
; a2.cfg := a2_get_user_config(a2data)

if (A_Args.Length) {
    args := _gather_args()
    Run '"' a2_ahk '" "' lib_path '\a2.ahk" ' args, root_path
}
else
    Run '"' a2_ahk '" "' lib_path '\a2.ahk"', root_path

; check_load_time_errors(lib_path)

If !FileExist(path_join(root_path, "_ user_data_include")) {
    ; Start the ui by default if there is no include file written yet.
    Run(path_join(root_path, "a2ui.exe"))
}

Return ; -----------------------------------------------------------------------
; check_load_time_errors(lib_path) {
;     script_name := "a2.ahk"
;     a2_popup := script_name " ahk_class #32770 ahk_exe Autohotkey.exe"
;     if !WinWaitActive(a2_popup,, 2)
;         return

;     ; win_id := WinExist(a2_popup)
;     ; idstr := "ahk_id " win_id
;     ctrl_txt := ControlGetText("Static1", a2_popup)
;     WinClose(a2_popup)
;     a2_on_startup_exception(ctrl_txt, path_join(lib_path, script_name))
; }

_gather_args() {
    args := ""
    for _, arg in A_Args {
        if InStr(arg, A_Space) {
            args .= string_quote(arg) . " "
        }
        else
            args .= arg . " "
    }
    return args
}

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
