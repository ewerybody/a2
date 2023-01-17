
; CONFIG_FILE_PATH := A_MyDocuments "\AutoHotkey\AutoHotkey.ini"
CONFIG_KEY := 'HKCU\Software\AutoHotkey'

ConfigRead(section, key, default) {
    ; return IniRead(CONFIG_FILE_PATH, section, key, default)
    return RegRead(CONFIG_KEY '\' section, key, default)
}

ConfigWrite(value, section, key) {
    ; IniWrite(value, CONFIG_FILE_PATH, section, key)
    RegWrite(value, 'REG_SZ', CONFIG_KEY '\' section, key)
}
