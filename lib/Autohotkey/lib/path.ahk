;a2 Autohotkey path library.

path_is_absolute(byref path) {
    ; Return true/false according to if given path is absolute or relative.
	SplitPath, path ,,,,, OutDrive
	if (OutDrive == "")
		return false
	else
		return true
}

path_dirname(byref path) {
    ; Return the parent directory to the path.
    SplitPath, path,, OutDir
    Return OutDir
}

path_basename(byref path) {
    ; Return the short-name of a given path without its path.
    SplitPath, path, OutFileName
    Return OutFileName
}

path_is_dir(byref path) {
    ; Return true/false according to if the given path exists and is a directory.
    if (InStr(FileExist(path), "D"))
        return true
    else
        return false
}

path_is_file(byref path) {
    ; Return true/false according to if the given path exists and is a file.
    attrs := FileExist(path)
    if (attrs != "" && !InStr(attrs, "D"))
        return true
    else
        return false
}

path_join(byref base_path, byref items) {
    ; Append two paths together and treat possibly double or missing backslashes
    path := RTrim(base_path, "\")
    Loop % items.Length()
        path := path "\" Trim(items[A_Index], "\")
    return path
}

path_normalize(byref path) {
    ; From the documentation - https://www.autohotkey.com/docs/misc/LongPaths.htm
    cc := DllCall("GetFullPathName", "str", path, "uint", 0, "ptr", 0, "ptr", 0, "uint")
    VarSetCapacity(buf, cc*2)
    DllCall("GetFullPathName", "str", path, "uint", cc, "str", buf, "ptr", 0)
    return buf
}

path_is_empty(byref path) {
    ; tell if the given path contains anything
    Loop, Files, %path%\*.*, FD
        return false
    return true
}


path_is_writeable(byref path) {
    FileGetAttrib, attr , %path%
    if InStr(attr, "R")
        return false
    return true
}

path_set_writable(byref path) {
    FileSetAttrib, -R, %path%
}

path_set_readonly(ByRef path) {
    FileSetAttrib, +R, %path%
}
