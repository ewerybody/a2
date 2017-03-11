; get_coordinates
#Persistent
;MsgBox A_ScriptDir: %A_ScriptDir%
tt("Left Mouse Button To Pick")

;CoordMode, Mouse, Screen|Window|Client]
CoordMode, Mouse, Screen

SetTimer, WatchCursor, 50

Escape::ExitApp
LButton::Gosub, PickCoordinates

return
#Include *i ..\ahklib\tt.ahk
#Include *i lib\ahklib\tt.ahk

WatchCursor:
    text := get_coords_str() "`nLeft Mouse Button To Pick`nEscape To Cancel"
    ;ToolTip, %text%
    global eZttText
    eZttText := text
return

get_coords_str() {
    MouseGetPos, mx, my
    data := mx ", " my
    return data
}

PickCoordinates:
    SetTimer, WatchCursor, Off
    global eZttText
    data := get_coords_str()
    FileAppend, %data%, *
    eZttText := data
    tt(data, 0.5,, 1)
Return
