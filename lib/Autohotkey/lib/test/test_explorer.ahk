#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include explorer.ahk
#Include window.ahk
#Include screen.ahk
#Include path.ahk
#Include string.ahk
#Include ahk_functions.ahk

explorers := explorer_window_list()
txt := "Found " explorers.Length() " explorer windows`n"
paths := get_explorer_paths(explorers)
txt .= "with" paths.Length() " different paths:`n  " string_join(paths, "`n  ")
Msgbox %txt%

; for i, win in explorers {
;     ; pid := win.pid
;     Process, Close, % win.pid
; }

; for i, path in paths
;     explorer_show(path)

Return

get_explorer_paths(explorers) {
    paths := []
    for i, win in explorers
    {
        path := explorer_get_path(win.id)
        if (string_is_in_array(path, paths))
            Continue
        paths.Push(path)
    }
    return paths
}
