;a2 Autohotkey path library.

; Return true/false according to if given path is absolute or relative.
path_is_absolute(byref path) {
	SplitPath, path ,,,,, OutDrive
	if (OutDrive == "")
		return false
	else
		return true
}

; Return the parent directory to the path.
path_dirname(byref path) {
    SplitPath, path,, OutDir
    Return OutDir
}

; Return the short-name of a given path without its path.
path_basename(byref path) {
    SplitPath, path, OutFileName
    Return OutFileName
}

; Return true/false according to if the given path exists and is a directory.
path_is_dir(byref path) {
    if (InStr(FileExist(path), "D"))
        return true
    else
        return false
}

; Return true/false according to if the given path exists and is a file.
path_is_file(byref path) {
    attrs := FileExist(path)
    if (attrs != "" && !InStr(attrs, "D"))
        return true
    else
        return false
}


; Append two paths together and treat possibly double or missing backslashes
path_join(byref base_path, byref items) {
    path := RTrim(base_path, "\")
    Loop % items.Length()
        path := path "\" Trim(items[A_Index], "\")
    return path
}


; From the documentation - https://www.autohotkey.com/docs/misc/LongPaths.htm
path_normalize(byref path) {
    cc := DllCall("GetFullPathName", "str", path, "uint", 0, "ptr", 0, "ptr", 0, "uint")
    VarSetCapacity(buf, cc*2)
    DllCall("GetFullPathName", "str", path, "uint", cc, "str", buf, "ptr", 0)
    return buf
}
