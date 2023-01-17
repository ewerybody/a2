
#include common.ahk

GetExeInfo(exe) {
    if !(verSize := DllCall("version\GetFileVersionInfoSize", "str", exe, "uint*", 0, "uint"))
        || !DllCall("version\GetFileVersionInfo", "str", exe, "uint", 0, "uint", verSize, "ptr", verInfo := Buffer(verSize))
        throw OSError()
    prop := {Path: exe}
    static Properties := {
        Version: 'FileVersion',
        Description: 'FileDescription',
        ProductName: 'ProductName'
    }
    for propName, infoName in Properties.OwnProps()
        if DllCall("version\VerQueryValue", "ptr", verInfo, "str", "\StringFileInfo\040904b0\" infoName, "ptr*", &p:=0, "uint*", &len:=0)
            prop.%propName% := StrGet(p, len)
        else throw OSError()
    if InStr(exe, '_UIA')
        prop.Description .= ' UIA'
    prop.Version := RegExReplace(prop.Version, 'i)[a-z]{2,}\K(?=\d)|, ', '.') ; Hack-fix for erroneous version numbers (AutoHotkey_H v2.0-beta3-H...)
    return prop
}

IsUsableAutoHotkey(exeinfo) {
    return exeinfo.HasProp('Description')
        && RegExMatch(exeinfo.Description, '^AutoHotkey.* (32|64)-bit', &m)
        && (m.1 != '64' || A_Is64bitOS)
        && !InStr(exeinfo.Path, '\AutoHotkeyUX.exe')
}

GetMajor(v) {
    Loop Parse, v, '.-+'
        return Integer(A_LoopField)
    throw ValueError('Invalid version number', -1, v)
}

ReadHashes(path, filter?) {
    filemap := Map(), filemap.CaseSense := 0
    if !FileExist(path)
        return filemap
    csvfile := FileOpen(path, 'r')
    props := StrSplit(csvfile.ReadLine(), ',')
    while !csvfile.AtEOF {
        item := {}
        Loop Parse csvfile.ReadLine(), 'CSV'
            item.%props[A_Index]% := A_LoopField
        if IsSet(filter) && !filter(item)
            continue
        filemap[item.Path] := item
    }
    return filemap
}

GetUsableAutoHotkeyExes() {
    static files
    if IsSet(files) {
        trace '![Launcher] returning hashes again'
        return files
    }
    files := ReadHashes(ROOT_DIR '\UX\installed-files.csv',
        item => IsUsableAutoHotkey(item) && (
            item.Path ~= '^(?!\w:|\\\\)' && item.Path := ROOT_DIR '\' item.Path,
            true
        ))
    if files.Count {
        trace '![Launcher] returning hashes from cache'
        return files
    }
    Loop Files ROOT_DIR '\AutoHotkey*.exe', 'R' {
        try {
            item := GetExeInfo(A_LoopFilePath)
            if IsUsableAutoHotkey(item)
                files[item.Path] := item
        }
    }
    trace '![Launcher] returning hashes from filesystem'
    return files
}
