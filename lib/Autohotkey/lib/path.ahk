path_is_absolute(byref path) {
	SplitPath, path ,,,,, OutDrive
	if (OutDrive == "")
		return false
	else
		return true
}

path_dirname(byref path) {
    SplitPath, path,, OutDir
    Return OutDir
}

path_basename(byref path) {
    SplitPath, path, OutFileName
    Return OutFileName
}

path_is_dir(byref path) {
    if (InStr(FileExist(path), "D"))
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
