dirname(byref path) {
    SplitPath, path,, OutDir
    Return OutDir
}


/**
 * Helper Function
 *     Expand path placeholders
 *     It's basically ExpandEnvironmentStrings() with some additional directories
 *
 * @sample
 *     ExpandPathPlaceholders("%ProgramFiles%")
 * @sample
 *     ExpandPathPlaceholders("Temp")
 * @sample
 *     ExpandPathPlaceholders("%Desktop%")
 *
 * @param   string  InputString     The path to be resolved
 * @return  string
 *
 * @docu   https://msdn.microsoft.com/en-us/library/windows/desktop/ms724265(v=vs.85).aspx
 */
ExpandPathPlaceholders(InputString)
{
    static Replacements := {  "Desktop" :             GetFullPathName(A_Desktop)
                            , "MyDocuments" :        GetFullPathName(A_MyDocuments)
                            , "StartMenu" :            GetFullPathName(A_StartMenu)
                            , "StartMenuCommon" :     GetFullPathName(A_StartMenuCommon)
                            , "a2Dir" :            A_ScriptDir "\.."}

    for Placeholder, Replacement in Replacements
        while(InStr(InputString, Placeholder) && A_Index < 10)
            StringReplace, InputString, InputString, % "%" Placeholder "%", % Replacement, All

    ; get the required size for the expanded string
    SizeNeeded := DllCall("ExpandEnvironmentStrings", "Str", InputString, "PTR", 0, "Int", 0)
    if (SizeNeeded == "" || SizeNeeded <= 0)
        return InputString ; unable to get the size for the expanded string for some reason

    ByteSize := SizeNeeded * 2 + 2
    VarSetCapacity(TempValue, ByteSize, 0)

    ; attempt to expand the environment string
    if (!DllCall("ExpandEnvironmentStrings", "Str", InputString, "Str", TempValue, "Int", SizeNeeded))
        return InputString ; unable to expand the environment string
    return TempValue
}

/**
 * Helper Function
 *     Converts the specified path to its long form.
 *
 * @sample
 *     GetFullPathName("C:\Progr~1")  -> "C:\Program Files"
 *
 * @param   string  sPath       The path to be converted.
 * @return  string
 *
 * @docu    https://msdn.microsoft.com/en-us/library/windows/desktop/aa364980(v=vs.85).aspx
 */
GetFullPathName(sPath)
{
    VarSetCapacity(lPath,A_IsUnicode ? 520 : 260, 0)
    DllCall("GetLongPathName", Str, sPath, Str, lPath, UInt, 260)
    return lPath
}

/**
 * Helper Function
 *     Formats a file size in bytes to a human-readable size string
 *
 * @sample
 *     x := FormatFileSize(31236)
 *
 * @param   int     Bytes      Number of bytes to be formated
 * @param   int     Decimals   Number of decimals to be shown
 * @param   int     Prefixes   List of which the best matching prefix will be used
 * @return  string
 */
FormatFileSize(Bytes, Decimals = 1, Prefixes = "B,KB,MB,GB,TB,PB,EB,ZB,YB")
{
    StringSplit, Prefix, Prefixes, `,
    Loop, Parse, Prefixes, `,
        if (Bytes < e := 1024 ** A_Index)
            return % Round(Bytes / (e / 1024), decimals) Prefix%A_Index%
}


; Append two paths together and treat possibly double or missing backslashes
AppendPaths(BasePath, RelativePath)
{
    if (!BasePath)
    return RelativePath
    if (!RelativePath)
    return BasePath
    return StringTrimLeft(BasePath, "\") "\" StringTrimLeft(RelativePath, "\")
}