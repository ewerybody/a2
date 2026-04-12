#Include <a2dlg>
#Include <explorer>
#Include <msgbox>
#Include <path>
#Include <screen>
#Include <string>
#Include <window>
#Include <windows>

explorer_example()
return

explorer_example() {
    dlg := A2Dialog("Explorer lib example", { w: 440 })

    explorers := window_list(, , "CabinetWClass")
    txt := "Found " explorers.Length " explorer windows`n"
    paths := _get_paths(explorers)
    txt .= "with " paths.Length " different paths:`n " string_join(paths, "`n ")

    dlg.text(txt)
    dlg.sep()

    dlg.text("Explore to Files:")
    buttons := dlg.btn_row([
        {label: "Single", func: _single},
        {label: "Multiple", func: _multi},
        {label: "Dir Only", func: _dirs}
    ])

    dlg.space(4)
    dlg.sep()
    dlg.btn_close()
    dlg.exit_on_close()
    dlg.esc_to_close()
    dlg.show()

    window_set_aot(true, dlg.hwnd)
}

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
    static lib_path := path_dirname(A_ScriptDir)
    static lib_files := path_get_files(lib_path,,1)

    select_files := []
    select_files.Push(lib_files[Random(1, lib_files.Length)])
    explorer_show(select_files*)
}

_multi(*) {
    static lib_path := path_dirname(A_ScriptDir)
    static lib_files := path_get_files(lib_path,,1)

    select_files := []
    while select_files.Length != 3 {
        this_file := lib_files[Random(1, lib_files.Length)]
        if string_is_in_array(this_file, select_files)
            continue
        select_files.Push(this_file)
    }
    explorer_show(select_files*)
}

_dirs(*) {
    static a2path := path_dirname(A_ScriptDir, 3)
    paths := []
    loop files a2path "\*", 'DR' {
        paths.push(A_LoopFileDir)
    }
    explorer_show(paths[Random(1, paths.Length)])
}
