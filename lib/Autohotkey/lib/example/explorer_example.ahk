#Include ..\windows.ahk
#Include ..\..\..\a2_globals.ahk
#Include %A_ScriptDir%\..\
#Include msgbox.ahk
#Include explorer.ahk
#Include window.ahk
#Include screen.ahk
#Include path.ahk
#Include string.ahk

explorers := window_list(,,"CabinetWClass")
if !(explorers.Length) {
    if not msgbox_accepted("For this test you need to have an Explorer Window open.`nOpen One?", "No Exploreres!")
        ExitApp

    explorer_show(A_ScriptDir)
    ; Sleep, 500
    WinWait("ahk_class CabinetWClass")
    Run "%A_AhkPath%" "%A_ScriptFullPath%", %A_ScriptDir%
    ExitApp
}

txt := "Found " explorers.Length " explorer windows`n"
paths := _get_paths(explorers)
txt .= "with " paths.Length " different paths:`n " string_join(paths, "`n ")

x1 := explorers[1]
selpths := explorer_get_selected(x1.id)
allpths := explorer_get_all(x1.id)
txt .= '`n`nExplorer 1: "' x1.title '" ID:' x1.id " PID:" x1.pid "`n"
txt .= "Selection: " selpths.Length " " string_join(selpths) "`nTotal number of items: " allpths.Length

msgbox_info(txt)

Return

_get_paths(explorers) {
    paths := []
    for i, win in explorers
    {
        path := explorer_get_path(win.id)
        if (!path or string_is_in_array(path, paths))
            Continue
        paths.Push(path)
    }
    return paths
}
