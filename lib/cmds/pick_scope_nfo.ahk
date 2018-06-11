; pick_scope_nfo
#Persistent
tt("Left Mouse Button To Pick")
CoordMode, Mouse, Screen
SetTimer, WatchCursor, 50

Escape::ExitApp
RButton::ExitApp
LButton::Gosub, PickInfo

return
#Include *i ..\ahklib\tt.ahk
#Include *i lib\ahklib\tt.ahk

WatchCursor:
    winfo := get_scope_info()
    text := "title: " winfo[1] "`nclass: " winfo[2] "`nprocess: " winfo[3] "`nLeft Mouse Button to pick`nEscape or Right Button to Cancel"
    global eZttText
    eZttText := text
return

get_scope_info() {
    MouseGetPos,,, window_id
	WinGetTitle, this_title, ahk_id %window_id%
	WinGetClass, this_class, ahk_id %window_id%
	WinGet, this_process, ProcessName, ahk_id %window_id%
    return [this_title, this_class, this_process]
}


PickInfo:
    SetTimer, WatchCursor, Off
    global eZttText
    winfo := get_scope_info()
    data := winfo[1] "`n" winfo[2] "`n" winfo[3]
    FileAppend, %data%, *
    eZttText := data
    tt(data, 0.5,, 1)
Return
