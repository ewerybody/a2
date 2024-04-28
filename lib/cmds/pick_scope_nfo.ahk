; pick_scope_nfo
Persistent
#include <a2tip>
a2tip("Left Mouse Button To Pick")
CoordMode "Mouse", "Screen"
SetTimer WatchCursor, 50

Escape::ExitApp
RButton::ExitApp
LButton::PickInfo

return

WatchCursor() {
    winfo := get_scope_info()
    text := "title: " winfo[1] "`nclass: " winfo[2] "`nprocess: " winfo[3] "`nLeft Mouse Button to pick`nEscape or Right Button to Cancel"
    ; TODO: fix a2tip!!
    a2tip(text)
    ; global eZttText
    ; eZttText := text
}


get_scope_info() {
    MouseGetPos ,, &window_id
    ahkid := "ahk_id " . window_id
	this_title := WinGetTitle(ahkid)
	this_class := WinGetClass(ahkid)
	this_process := WinGetProcessName(ahkid)
    return [this_title, this_class, this_process]
}


PickInfo() {
    SetTimer WatchCursor, 0
    global eZttText
    winfo := get_scope_info()
    data := winfo[1] "`n" winfo[2] "`n" winfo[3]
    FileAppend(data, "*")
    eZttText := data
    a2tip(data, 0.5)
}
