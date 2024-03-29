#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include explorer.ahk
#Include window.ahk
#Include screen.ahk
#Include path.ahk
#Include string.ahk
#Include ahk_functions.ahk

explorers := window_list(,,"CabinetWClass")
if !(explorers.Length()) {
    MsgBox, 33, No Exploreres!, For this test you need to have an Explorer Window open.`nOpen One?
        IfMsgBox, Cancel
    ExitApp

    explorer_show(A_ScriptDir)
    ; Sleep, 500
    WinWait, ahk_class CabinetWClass
    Run, "%A_AhkPath%" "%A_ScriptFullPath%", %A_ScriptDir%
    ExitApp
}

txt := "Found " explorers.Length() " explorer windows`n"
paths := _get_paths(explorers)
txt .= "with " paths.Length() " different paths:`n " string_join(paths, "`n ")

x1 := explorers[1]
selpths := explorer_get_selected(x1.id)
allpths := explorer_get_all(x1.id)
txt .= "`n`nExplorer 1: """ x1.title """ " x1.id " " x1.pid "`n"
txt .= "Selection: " selpths.Length() " " string_join(selpths) "`nTotal number of items: " allpths.Length()

Msgbox %txt%

Return

_get_paths(explorers) {
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
