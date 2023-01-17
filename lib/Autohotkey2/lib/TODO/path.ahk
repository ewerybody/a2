﻿;a2 Autohotkey path library.
#include ahk_functions.ahk

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

path_split_ext(byref path) {
    ; Return No-extension file name and extension in a list.
    SplitPath, path,,, OutExtension, OutNameNoExt
    Return [OutNameNoExt, OutExtension]
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

path_join(byref base_path, byref items*) {
    ; Append two paths together and treat possibly double or missing backslashes
    ; Now Variadic! https://www.autohotkey.com/docs/Functions.htm#Variadic
    path := RTrim(base_path, "\")
    Loop % items.Length()
        path .= "\" Trim(items[A_Index], "\")
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
    if InStr(FileGetAttrib(path), "R")
        return false
    return true
}

path_set_writable(byref path) {
    FileSetAttrib, -R, %path%
}

path_set_readonly(ByRef path) {
    FileSetAttrib, +R, %path%
}

path_expand_env(byref path) {
    ; Find environment %variables% in a path,
    ; Return expanded path string.
    if !InStr(path, "%")
        Return path

    pos1 := InStr(path, "%")
    pos2 := InStr(path, "%",, pos1 + 1)
    if !pos2
        Return path
    subs := SubStr(path, pos1 + 1, pos2 - pos1 - 1)
    env_path := EnvGet(subs)
    new_path := StrReplace(path, "%" subs "%", env_path)
    ; MsgBox pos1: %pos1%`npos2: %pos2%`nsubs: %subs%`nenv_path: %env_path%`nnew_path: %new_path%
    return new_path
}

path_neighbor(file_path, neighbor_name) {
    ; Shorthand to do `path_join(path_dirname(file_path), "somename.txt")`.
    ; Also handy with builtin var `A_LineFile`!
    return path_join(path_dirname(file_path), neighbor_name)
}

; If already existing add numbers to file name until a free one is found.
path_get_free_name(dir_path, file_name, ext, separator := "") {
    if !file_name AND !ext
        Return file_name

    ext := string_prefix(Trim(ext), ".")
    file_path := path_join(dir_path, file_name . ext)
    if !FileExist(file_path)
        Return file_name

    index := 1
    While, FileExist(file_path) {
        index++
        base := file_name . separator . index
        file_path := path_join(dir_path, base . ext)
    }
    return base
}
