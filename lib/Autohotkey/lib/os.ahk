file_dirname(byref path) {
    SplitPath, path,, OutDir
    Return OutDir
}

file_basename(byref path) {
    SplitPath, path, OutFileName
    Return OutFileName
}

files_in_clipboard() {
    files := StrSplit(Clipboard, "`r`n")
    is_files := true
    for i, item in files {
        if !FileExist(item) {
            is_files := false
            Break
        }
    }

    if (is_files)
        return files
}

is_dir(byref path) {
    return (InStr(FileExist(path), "D"))? true : false
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
JoinPath(BasePath, RelativePath)
{
    if (!BasePath)
        return RelativePath
    if (!RelativePath)
        return BasePath
    return StringTrimLeft(BasePath, "\") "\" StringTrimLeft(RelativePath, "\")
}
