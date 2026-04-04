#Include ..\windows.ahk
#Include ..\..\..\a2_globals.ahk
#Include %A_ScriptDir%\..\
#Include <a2dlg>
#Include <msgbox>
#Include <explorer>
#Include <window>
#Include <screen>
#Include <path>
#Include <string>

explorer_example()

explorer_example() {
    dlg := A2Dialog("Explorer lib example", { w: 440 })

    explorers := window_list(, , "CabinetWClass")
    txt := "Found " explorers.Length " explorer windows`n"
    paths := _get_paths(explorers)
    txt .= "with " paths.Length " different paths:`n " string_join(paths, "`n ")

    dlg.text(txt)
    dlg.sep()

    dlg.text("Explore to Files:")
    ; dlg.btn_row()
    buttons := dlg.btn_row([
        {label: "Single"}, {label: "Multiple"}, {label: "Multi Dirs"}, {label: "Dir Only"}
    ])
    buttons[1].OnEvent("Click", _single)
    buttons[2].OnEvent("Click", _multi)

    dlg.space(4)
    dlg.sep()
    dlg.btn_close()
    dlg.exit_on_close()
    dlg.esc_to_close()
    dlg.show()

    window_set_aot(true, dlg.hwnd)
}

; x1 := explorers[1]
; sel_paths := explorer_get_selected(x1.id)
; all_paths := explorer_get_all(x1.id)
; txt .= '`n`nExplorer 1: "' x1.title '" ID:' x1.id " PID:" x1.pid "`n"
; txt .= "Selection: " sel_paths.Length " " string_join(sel_paths) "`nTotal number of items: " all_paths.Length

; msgbox_info(txt)

return

_get_paths(explorers) {
    paths := []
    for i, win in explorers {
        path := explorer_get_path(win.id)
        if (!path or string_is_in_array(path, paths))
            continue
        paths.Push(path)
    }
    return paths
}

_single(*) {
    static a2path := path_dirname(A_ScriptDir)
    static lib_files := path_get_files(a2path,,1)

    select_files := []
    select_files.Push(lib_files[Random(1, lib_files.Length)])
    explorer_show(select_files*)
}

_multi(*) {
    static a2path := path_dirname(A_ScriptDir)
    static lib_files := path_get_files(a2path,,1)

    select_files := []
    while select_files.Length != 3 {
        this_file := lib_files[Random(1, lib_files.Length)]
        if string_is_in_array(this_file, select_files)
            continue
        select_files.Push(this_file)
    }
    explorer_show(select_files*)
}