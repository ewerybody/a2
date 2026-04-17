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
#Include <a2dlg>
#Include <path>


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
    ; thanks to PolyEthene
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

; Set the path of the target Explorer window.
explorer_set_path(path, hwnd:="") {
    if !(window := explorer_get_window(hwnd))
        return ErrorLevel := "ERROR"
    if (window == "desktop" OR !path_is_dir(path))
        return

    window.Navigate(path)
}


; Get array of paths of ALL items via Explorer window handle.
explorer_get_all(hwnd:="") {
    return explorer_get(hwnd)
}

; Get Explorer window COM object from handle.
explorer_get_window(hwnd:="") {
    ; Thanks to JeThrow for some pointers here!
    ; WinGet proc, processName, "ahk_id " hwnd := hwnd? hwnd:
    if not hwnd
        hwnd := WinExist("A")

    if (WinGetProcessName("ahk_id " . hwnd) != "explorer.exe")
        return

    this_class := WinGetClass("ahk_id " . hwnd)
    if (this_class ~= "(Cabinet|Explore)WClass") {
        for window in ComObject("Shell.Application").Windows
            Try if (window.hwnd==hwnd)
            return window
    }
    else if (this_class ~= "Progman|WorkerW")
        return "desktop" ; desktop found
    else if (this_class == "Shell_TrayWnd")
        return
}

; Get items from an Explorer window via handle.
explorer_get(hwnd := "", selection := false) {
    result := []
    if !(window := explorer_get_window(hwnd))
        return result

    if (window=="desktop") {
        hwWindow := ControlGetHwnd("SysListView321", "ahk_class Progman")
        if !hwWindow ; #D mode
            hwWindow := ControlGetHwnd("SysListView321", "A")

        ctrl := "Col1"
        if selection
            ctrl := "Selected" . ctrl

        ; ControlGet files, List, ( selection ? "Selected":"") "Col1",,%
        files := ControlGetItems(ctrl, "ahk_id " . hwWindow)
        base := SubStr(A_Desktop,0,1)=="\" ? SubStr(A_Desktop,1,-1) : A_Desktop
        for item in files {
            path := base "\" item
            if FileExist(path) ; ignore special icons like Computer (at least for now)
                result.Push(path)
        }
    } else {
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

    base_names := []
    if IsObject(basename) {
        for name in basename
            base_names.push(path_basename(name))
    } else {
        base_names.push(path_basename(basename))
    }

    file_found := 0
    for item in window.document.Folder.Items {
        ; Cannot use item.name because of possibly hidden extensions.
        ; Yep. There is no explicit "item.name_WITH_ext" m(
        ; https://docs.microsoft.com/en-us/windows/win32/shell/folderitem#properties
        if (string_is_in_array(path_basename(item.path), base_names)) {
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

    Loop retries {
        if explorer_select(basename)
            Return 1
        Sleep delay
    }

    return 0
}

; Open Windows Explorer with the given directory or directory with file(s) selected.
explorer_show(paths*) {
    for dir_path, files in path_get_dir_map(paths)
        explorer_show_dir_files(dir_path, files)
}

; Explicitly open Windows Explorer with a given directory path.
explorer_show_dir(path) {
    if !path_is_dir(path)
        throw Error("explorer_show_dir needs an existing directory path!")
    Run("open " path)
}

; Call SHOpenFolderAndSelectItems with given `dir_path` and selected `files` in it.
explorer_show_dir_files(dir_path, files) {
    if !files.Length {
        explorer_show_dir(dir_path)
        return
    }

    ; Folder PIDL + COM init
    dir_path := StrReplace(RTrim(dir_path, "\"), "\\", "\")
    hr_init := DllCall("ole32\CoInitializeEx", "Ptr", 0, "UInt", 2, "HRESULT")  ; COINIT_APARTMENTTHREADED
    try {
        DllCall("shell32\SHParseDisplayName",
            "Str", dir_path, "Ptr", 0, "Ptr*", &folder_p_id_list := 0, "UInt", 0, "Ptr", 0,
            "HRESULT")
    } catch Error as dll_error{
        a2dlg_error('Error DllCalling "shell32\SHParseDisplayName"',,
            "dir_path: '" dir_path "'`n"
        )
        throw dll_error
    }

    ; Build PIDL array for files
    item_list := Buffer(files.Length * A_PtrSize)
    for i, f in files {
        f_path := dir_path "\" f
        DllCall("shell32\SHParseDisplayName",
            "Str", f_path, "Ptr", 0, "Ptr*", &p_id_list := 0, "UInt", 0, "Ptr", 0,
            "HRESULT")
        NumPut("Ptr", p_id_list, item_list, (i - 1) * A_PtrSize)
    }

    DllCall("shell32\SHOpenFolderAndSelectItems",
        "Ptr", folder_p_id_list, "UInt", files.Length, "Ptr", item_list, "UInt", 0,
        "HRESULT")

    ; Cleanup
    DllCall("ole32\CoTaskMemFree", "Ptr", folder_p_id_list)
    loop files.Length
        DllCall("ole32\CoTaskMemFree", "Ptr", NumGet(item_list, (A_Index - 1) * A_PtrSize, "Ptr"))
    if hr_init == 0
        DllCall("ole32\CoUninitialize")
}

/**
 * Ask for file name as long that name exists in given directory or user cancels.
 * Return `true` if name is available and accepted and `false` if canceled.
 *
 * @param file_name
 * @param dir_path
 * @param extension
 * @param file_label
 * @param title
 * @param subtitle
 * @param w
 * @param h
 */
explorer_create_file_dialog(&file_name, dir_path, extension, file_label, title, subtitle := "", w := 420, h:= 140)
{
    if (!dir_path) {
        a2dlg_error("No dir_path given!")
        Return
    }

    extension := Trim(string_prefix(extension, "."))
    extension := StrLower(extension)

    msg := "Please enter a name for the new " file_label ":`n"
    result := a2dlg_input(msg . subtitle, title, file_name)
    if !result
        Return false

    file_name := result
    file_path := __create_dialog_build_path(dir_path, file_name, extension)
    while (Trim(file_name) == "" OR FileExist(file_path)) {
        if FileExist(file_path)
            msg := "This file name already exists! Please pick another " file_label " name!`n"
        else
            msg := "Please enter NON-EMPTY name for the new " file_label ":`n"

        result := a2dlg_input(msg . subtitle, title, file_name)
        if !result
            Return false

        file_path := __create_dialog_build_path(dir_path, result, extension)
    }
    Return true
}

__create_dialog_build_path(dir_path, file_name, extension)
{
    this_ext := path_split_ext(file_name)[2]
    if this_ext {
        this_ext := StrLower(this_ext)
        this_ext := Trim(string_prefix(this_ext, "."))

        if (this_ext == extension) {
            Return path_join(dir_path, file_name)
        }
    }
    Return path_join(dir_path, file_name extension)
}
