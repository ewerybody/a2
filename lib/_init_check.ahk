; a2 _init_check. This is used by a2_starter and is not supposed to be run standalone
_INIT_ERR_STARTER = _init_check.ahk is only to be used by compiled a2_starter!
;MsgBox A_ScriptName: %A_ScriptName%`nA_IsCompiled: %A_IsCompiled%
if (!A_IsCompiled || (A_ScriptName != "a2_starter.exe")) {
    MsgBox, 16, _init_check.ahk, %_INIT_ERR_STARTER%
    ExitApp
}

_init_check_settings() {
    lib_ahk = lib\AutoHotkey\AutoHotkey.exe
    lib_ahk_path = %A_ScriptDir%\%lib_ahk%
    ;RegRead, installed_ahk, HKEY_LOCAL_MACHINE, SOFTWARE\AutoHotkey, InstallDir
    ;installed_ahk = %installed_ahk%\AutoHotkey.exe
    ;MsgBox installed_ahk: %installed_ahk%
    IfNotExist, %lib_ahk_path%
    {
        MsgBox, 16, ERROR - AutoHotkey.exe not available, So I wanted to create vanilla a2 settings, but seems 
    }
    
    FileGetVersion, version, %installed_ahk%
    MsgBox version: %version%
}