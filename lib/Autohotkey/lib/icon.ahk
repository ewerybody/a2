/**
 * Extract an icon from an executable, DLL or icon file.
 * @example
 *      icon_extract("C:\windows\system32\system.dll", 1)
 *
 * @param {(String)} filename
 * Name of the ico, dll or exe from which to extract the icon
 * @param {(Integer)} icon_number
 * 1-based index of the icon in the file
 * @param {(Integer)} icon_size
 * Resolution of the icon (e.g. 16, 32, 48, 64)
 * @returns  HICON handle, or 0 on failure
*/
icon_extract(filename, icon_number := 1, icon_size := 32) {
    try {
        h_icon := 0
        r := DllCall("Shell32.dll\SHExtractIconsW",
            "str",  filename,
            "int",  icon_number - 1,  ; API is 0-based
            "int",  icon_size,
            "int",  icon_size,
            "Ptr*", &h_icon,
            "Ptr",  0,               ; pIconId — not needed, pass NULL
            "uint", 1,               ; nIcons
            "uint", 0,               ; flags
            "uint")                  ; return type: UINT (number of icons extracted)
        return (r > 0 && h_icon) ? h_icon : 0
    } catch {
        return 0
    }
}

/**
 * Return the number of icons stored in a DLL, EXE, or ICO file.
 * @example
 *      icon_get_icon_count("C:\Windows\System32\imageres.dll")
 *
 * @param {(String)} filename
 * Path to the DLL, EXE, or ICO file to inspect
 * @returns  Icon count, or 0 if the file has no icons or cannot be read
*/
icon_get_icon_count(filename) {
    try {
        return DllCall("Shell32.dll\ExtractIconExW",
            "str",  filename,
            "int",  -1,    ; special: return count instead of extracting
            "Ptr",  0,     ; pHiconLarge = NULL
            "Ptr",  0,     ; pHiconSmall = NULL
            "uint", 0,     ; nIcons
            "uint")        ; return type: UINT
    } catch {
        return 0
    }
}

/**
 * Resolve the registered icon path for a file extension via the Windows registry.
 * Checks per-user app associations (UserChoice) before falling back to HKCR.
 * @example
 *      icon_from_type("pdf")   ; => "C:\...\firefox.exe,5"
 *
 * @param {(String)} extension
 * File extension with or without leading dot (e.g. "pdf" or ".pdf")
 * @returns  Registry icon path string, or "" if unregistered or no icon found
*/
icon_from_type(extension) {
    extension := string_prefix(extension, ".")
    user_choice_key := "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\"
        . extension . "\UserChoice"
    try prog_id := RegRead(user_choice_key, "ProgId")
    if IsSet(prog_id) && prog_id {
        icon := _icon_from_progid(prog_id)
        if icon
            return icon
    }
    try typ := RegRead(path_join("HKCR", extension))
    if !IsSet(typ) || !typ
        return ""
    return _icon_from_progid(typ)
}

/**
 * Split a Windows registry icon path into a file path and an AHK picture option.
 * Registry paths use "file.exe,N" with a 0-based index; AHK AddPicture expects
 * "IconN" (1-based) in the options string.
 * @example
 *      p := icon_path_split("C:\...\firefox.exe,5")
 *      gui.AddPicture("w32 h32 " p.opt, p.file)
 *
 * @param {(String)} path
 * Registry icon path, e.g. "C:\Windows\System32\shell32.dll,2"
 * @returns  Object {file, opt} — opt is "" for paths without an index
*/
icon_path_split(path) {
    if !InStr(path, ",")
        return {file: path, opt: ""}
    parts := StrSplit(path, ",", , 2)
    try n := Integer(parts[2])
    if !IsSet(n)
        return {file: parts[1], opt: ""}
    ; Registry is 0-based; AHK Icon1 = first icon. Negative resource IDs are the same.
    return {file: parts[1], opt: "Icon" (n >= 0 ? n + 1 : n)}
}

/**
 * Resolve a ProgId to an icon path via HKCR.
 * Tries DefaultIcon first; falls back to the exe path from shell\open\command.
 *
 * @param {(String)} prog_id
 * ProgId / type name, e.g. "FirefoxPDF-CA9422711AE1A81C"
 * @returns  Icon path string, or "" if nothing is found
*/
_icon_from_progid(prog_id) {
    try icon := RegRead(path_join("HKCR", path_join(prog_id, "DefaultIcon")))
    if !IsSet(icon) || !icon {
        try icon := RegRead(path_join("HKCR", path_join(prog_id, "shell\open\command")))
        if IsSet(icon) && string_startswith(icon, '"')
            icon := SubStr(icon, 2, InStr(icon, '"' ,, 2) - 2)
    }
    return IsSet(icon) ? icon : ""
}
