/**
 * Helper Function
 *     Extract an icon from an executable, DLL or icon file.
 *
 * @sample
 *     icon_extract("C:\windows\system32\system.dll", 1)
 *
 * @param   string  Filename    Name of the ico, dll or exe from which to extract the icon
 * @param   integer IconNumber  Index of the icon in the file
 * @param   integer IconSize    Resolution of the icon
 * @return  bitmap
*/
icon_extract(Filename, IconNumber = 0, IconSize = 64) {
    ; LoadImage is not used..
    ; ..with exe/dll files because:
    ;   it only works with modules loaded by the current process,
    ;   it needs the resource ordinal (which is not the same as an icon index), and
    ; ..with ico files because:
    ;   it can only load the first icon (of size %IconSize%) from an .ico file.

    ; If possible, use PrivateExtractIcons, which supports any size of icon.
    ; r:=DllCall("PrivateExtractIcons" , "str", Filename, "int", IconNumber-1, "int"
    ; , IconSize, "int", IconSize, "Ptr*", h_icon, "PTR*", 0, "uint", 1, "uint", 0, "int")
    ; if !ErrorLevel
    ;    return h_icon
    r := DllCall("Shell32.dll\SHExtractIconsW", "str", Filename, "int", IconNumber-1, "int"
    , IconSize, "int", IconSize, "Ptr*", h_icon, "Ptr*", pIconId, "uint", 1, "uint", 0, "int")
    If (!ErrorLevel && r != 0)
        return h_icon
    return 0
}

icon_from_type(extension) {
    ; Try looking up Windows registry in CLASSES ROOT for given extension.
    ; Find DefaultIcon, return path if any, if not:
    ; Find shell/open/command, return path
    extension := string_prefix(extension, ".")
    typ := RegRead(path_join("HKCR", extension))
    def_icon_pth := path_join(typ, "DefaultIcon")
    icon := RegRead(path_join("HKCR", def_icon_pth))
    if (!icon) {
        icon := RegRead(path_join("HKCR", path_join(typ, "shell\open\command")))
        if string_startswith(icon, '"') {
            icon := SubStr(icon, 2, InStr(icon, '"' ,, 2) - 2)
        }
    }
    return icon
}
