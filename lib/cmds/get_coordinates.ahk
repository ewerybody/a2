; get_coordinates
#Persistent
msg := "`nLeft Mouse Button To Pick`nEscape To Cancel"
a2tip(msg)
cursor_set_cross()
CoordMode, Mouse, Screen

SetTimer, WatchCursor, 50

Escape::Gosub, Exit
LButton::Gosub, PickCoordinates

return

WatchCursor:
    text := get_coords_str() . msg
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
    cursor_reset()
    global eZttText
    data := get_coords_str()
    FileAppend, %data%, *
    eZttText := data
    a2tip(data, 0.5,, 1)
Return

Exit:
    cursor_reset()
    ExitApp
Return