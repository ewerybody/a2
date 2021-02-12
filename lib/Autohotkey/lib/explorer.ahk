/*
	Library for getting info from a specific explorer window (if window handle not specified, the currently active
	window will be used).  Requires AHK_L or similar.  Works with the desktop.  Does not currently work with save
	dialogs and such.

	example:
		F1::
			path := explorer_get_path()
			all := explorer_get_all()
			sel := explorer_get_selected()
			MsgBox % path
			MsgBox % all
			MsgBox % sel
		return

	Joshua A. Kinnison
	2011-04-27, 16:12
*/

explorer_get_selected(hwnd="") {
    ; Get paths of target window's selected items.
    return explorer_get(hwnd, true)
}

explorer_get_path(hwnd="") {
    ; Get path of target window's folder.
    if !(window := explorer_get_window(hwnd))
        return ErrorLevel := "ERROR"
    if (window="desktop")
        return A_Desktop
    path := window.LocationURL
    path := RegExReplace(path, "ftp://.*@", "ftp://")
    StringReplace, path, path, file:///
    StringReplace, path, path, /, \, All

    ; thanks to polyethene
    Loop
        If RegExMatch(path, "i)(?<=%)[\da-f]{1,2}", hex)
        StringReplace, path, path, `%%hex%, % Chr("0x" . hex), All
    Else Break
        return path
}

explorer_get_all(hwnd="") {
    ; Get paths of all items in the target window's folder.
    return explorer_get(hwnd)
}

explorer_get_window(hwnd="")
{
    ; thanks to jethrow for some pointers here
    WinGet, process, processName, % "ahk_id" hwnd := hwnd? hwnd:WinExist("A")
    WinGetClass class, ahk_id %hwnd%

    if (process!="explorer.exe")
        return

    if (class ~= "(Cabinet|Explore)WClass")
    {
        for window in ComObjCreate("Shell.Application").Windows
            Try if (window.hwnd==hwnd)
            return window
    }
    else if (class ~= "Progman|WorkerW")
        return "desktop" ; desktop found
}

explorer_get(hwnd="",selection=false)
{
    if !(window := explorer_get_window(hwnd))
        return ErrorLevel := "ERROR"

    if (window="desktop")
    {
        ControlGet, hwWindow, HWND,, SysListView321, ahk_class Progman
        if !hwWindow ; #D mode
            ControlGet, hwWindow, HWND,, SysListView321, A
        ControlGet, files, List, % ( selection ? "Selected":"") "Col1",,ahk_id %hwWindow%
        base := SubStr(A_Desktop,0,1)=="\" ? SubStr(A_Desktop,1,-1) : A_Desktop
        Loop, Parse, files, `n, `r
        {
            path := base "\" A_LoopField
            IfExist %path% ; ignore special icons like Computer (at least for now)
                ret .= path "`n"
        }
    }
    else
    {
        if selection
            collection := window.document.SelectedItems
        else
            collection := window.document.Folder.Items
        for item in collection
            ret .= item.path "`n"
    }

    return Trim(ret)
}

explorer_select(basename) {
    ; Selects a file with the given basename
    if !(window := explorer_get_window(hwnd))
        return ErrorLevel := "ERROR"
    file_found := 0
    for item in window.document.Folder.Items
    {
        if (item.name == basename)
        {
            window.document.SelectItem(item, 1)
            file_found := 1
        } else {
            window.document.SelectItem(item, 0)
        }
    }
    return file_found
}

explorer_show(path) {
    ; Open an Explorer with the given directory or file selected.
    path := StrReplace(path, "\\", "\")

    explorer_path := path_join(A_WinDir, "explorer.exe")
    if path_is_file(path)
        cmd := """" . explorer_path . """ /select, """ . path . """"
    else if path_is_dir(path)
        cmd := """" . explorer_path . """ """ . path . """"
    else
        MsgBox, No such path to explorer to!`n %path%

    Run, %cmd%
}
