; get_coordinates.ahk
#Include <a2tip>
#Include <cursor>

Persistent
MSG := "`nLeft Mouse Button To Pick`nEscape To Cancel"
a2tip(MSG, -1)
cursor_set_cross()
CoordMode("Mouse", "Screen")

SetTimer(WatchCursor, 50)

Escape::Exit
~LButton::PickCoordinates
return

WatchCursor() {
    text := get_coords_str() MSG
    global a2tip_message
    a2tip_message := text
}

get_coords_str() {
    MouseGetPos(&mx, &my)
    data := mx ", " my
    return data
}

PickCoordinates() {
    SetTimer(WatchCursor, 0)
    cursor_reset()
    data := get_coords_str()
    FileAppend(data, "*")
    Exit()
}

Exit() {
    cursor_reset()
    ExitApp
}
