/**
 * Get the version ID of the current Windows installation
 * @return {(integer)}
 */
windows_get_version()
{
    Version := DllCall("GetVersion", "uint") & 0xFFFF
    return (Version & 0xFF) "." (Version >> 8)
}

/**
 * True when Windows "Apps use dark mode" is on.
 * @returns {(Boolean)}
 */
windows_is_dark() {
    try return !RegRead("HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "AppsUseLightTheme")
    return false
}

/**
 * Tell windows what kind of theme to take for our process.
 * @param {(Integer)} mode
 * Either 0 or 1 for light or dark theme mode.
 */
windows_set_theme(mode := 1) {
    hUxTheme := DllCall("GetModuleHandle", "str", "uxtheme", "ptr")
    DllCall(DllCall("GetProcAddress", "ptr", hUxTheme, "ptr", 135, "ptr"), "int", mode)
    DllCall(DllCall("GetProcAddress", "ptr", hUxTheme, "ptr", 136, "ptr"))
}
