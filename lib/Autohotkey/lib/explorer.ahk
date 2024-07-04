/* Extended a2 Windows File Explorer Library
for getting info from a specific Explorer window.

Original:
... If window handle not specified, the currently active window will be used.
Works with the desktop. Does not currently work with save dialogs and such.

examples:
	path := explorer_get_path()
	all := explorer_get_all()
	sel := explorer_get_selected()

Joshua A. Kinnison
2011-04-27, 16:12
*/

; Get array of paths of selected items via Explorer window handle.
explorer_get_selected(hwnd:="") {
    return explorer_get(hwnd, true)
}

; Get path of target window's folder.
explorer_get_path(hwnd:="") {
    if !(window := explorer_get_window(hwnd))
        return ErrorLevel := "ERROR"
    if (window="desktop")
        return A_Desktop
    pth := RegExReplace(window.LocationURL, "ftp://.*@", "ftp://")
    pth := StrReplace(pth, "file:///", "")
    pth := StrReplace(pth, "/", "\")
    ; thanks to polyethene
    Loop
    {
        ; find "%20" patterns. That's 2 hex digits after a %
        RegExMatch(pth, "i)(?<=%)[\da-f]{1,2}", &match)
        If (!match)
            Break
        pth := StrReplace(pth, "%" . match[0], Chr("0x" . match[0]))
    }
    return pth
}

; Get array of paths of ALL items via Explorer window handle.
explorer_get_all(hwnd:="") {
    return explorer_get(hwnd)
}

; Get Explorer window COM object from handle.
explorer_get_window(hwnd:="") {
    ; Thanks to jethrow for some pointers here!
    ; WinGet proc, processName, "ahk_id " hwnd := hwnd? hwnd:
    if not hwnd
        hwnd := WinExist("A")

    if (WinGetProcessName("ahk_id " . hwnd) != "explorer.exe")
        return

    clss := WinGetClass("ahk_id " . hwnd)
    if (clss ~= "(Cabinet|Explore)WClass") {
        for window in ComObject("Shell.Application").Windows
            Try if (window.hwnd==hwnd)
            return window
    }
    else if (clss ~= "Progman|WorkerW")
        return "desktop" ; desktop found
    else if (clss == "Shell_TrayWnd")
        return
}

; Get items from an Explorer window via handle.
explorer_get(hwnd:="",selection:=false) {
    if !(window := explorer_get_window(hwnd))
        return ErrorLevel := "ERROR"

    result := []
    if (window=="desktop")
    {
        hwWindow := ControlGetHwnd("SysListView321", "ahk_class Progman")
        if !hwWindow ; #D mode
            hwWindow := ControlGetHwnd("SysListView321", "A")

        ctrl := "Col1"
        if selection
            ctrl := "Selected" . ctrl

        ; ControlGet files, List, ( selection ? "Selected":"") "Col1",,%
        files := ControlGetItems(ctrl, "ahk_id " . hwWindow)
        base := SubStr(A_Desktop,0,1)=="\" ? SubStr(A_Desktop,1,-1) : A_Desktop
        for item in files
        ; Loop Parse, files, '`n', '`r'
        {
            path := base "\" item
            if FileExist(path) ; ignore special icons like Computer (at least for now)
                result.Push(path)
        }
    }
    else
    {
        if selection
            collection := window.document.SelectedItems
        else
            collection := window.document.Folder.Items

        for item in collection
            result.Push(item.path)
    }
    return result
}

; Select a file or folder with the given basename.or path in the current explorer
explorer_select(basename) {
    if !(window := explorer_get_window(""))
        return ErrorLevel := "ERROR"

    basenames := []
    if IsObject(basename) {
        for name in basename
            basenames.push(path_basename(name))
    } else {
        basenames.push(path_basename(basename))
    }

    file_found := 0
    for item in window.document.Folder.Items
    {
        ; Cannot use item.name because of possibly hidden extensions.
        ; Yep. There is no explicit "item.name_WITH_ext" m(
        ; https://docs.microsoft.com/en-us/windows/win32/shell/folderitem#properties
        if (string_is_in_array(path_basename(item.path), basenames))
        {
            window.document.SelectItem(item, 1)
            file_found := 1
        } else {
            window.document.SelectItem(item, 0)
        }
    }
    return file_found
}

; Try and retry selecting a file for a couple times.
explorer_try_select(basename, retries := 10, delay := 500) {

    Loop retries
    {
        if explorer_select(basename)
            Return 1
        Sleep delay
    }

    return 0
}

; Open an Explorer with the given directory or file selected.
explorer_show(pth) {
    pth := StrReplace(pth, "\\", "\")
    pth := StrReplace(pth, "/", "\")

    explorer_path := path_join(A_WinDir, "explorer.exe")
    if path_is_file(pth)
        cmd := '"' explorer_path '" /select, "' pth '"'
    else if path_is_dir(pth)
        cmd := '"' explorer_path '" "' pth '"'
    else if (pth == "") {
        cmd := '"' explorer_path '"'
    }
    else
        msgbox_error("No such path to explorer to!`n " . pth)

    Run cmd
}

; Ask for file name as long that name exists in given directory or user cancels. Return `true` if name is available and accepted and `false` if canceled.
explorer_create_file_dialog(&file_name, dir_path, extension, file_label, title, subtitle := "", w := 420, h:= 140)
{
    if (!dir_path) {
        msgbox_error("No dir_path given!")
        Return
    }

    extension := Trim(string_prefix(extension, "."))
    extension := StrLower(extension)

    msg := "Please enter a name for the new " file_label ":`n"
    ibx := InputBox(msg . subtitle, title, "w420 h140", file_name)
    if ibx.Result = "Cancel"
        Return false

    file_name := ibx.value
    file_path := __create_dialog_build_path(dir_path, file_name, extension)
    while (Trim(file_name) == "" OR FileExist(file_path)) {
        if FileExist(file_path)
            msg := "This file name already exists! Please pick another " file_label " name!`n"
        else
            msg := "Please enter NON-EMPTY name for the new " file_label ":`n"

        ibx := InputBox(msg . subtitle, title, "w420 h140", file_name)
        if ibx.Result = "Cancel"
            Return false

        file_path := __create_dialog_build_path(dir_path, ibx.value, extension)
    }
    Return true
}

__create_dialog_build_path(dir_path, file_name, extension)
{
    this_ext := path_split_ext(file_name)[2]
    if this_ext
    {
        this_ext := StrLower(this_ext)
        this_ext := Trim(string_prefix(this_ext, "."))

        if (this_ext == extension) {
            Return path_join(dir_path, file_name)
        }
    }
    Return path_join(dir_path, file_name extension)
}
