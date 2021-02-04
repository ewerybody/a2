#Include %A_ScriptDir%\..\ahk_functions.ahk
#Include %A_ScriptDir%\..\window.ahk
#Include %A_ScriptDir%\..\screen.ahk

win_id := WinExist("A")
geo := window_get_geometry(win_id)
geo_str := geo.x " " geo.y " " geo.w " " geo.h
crect := GetClientRect(win_id)
crect_str := crect.x " " crect.y " " crect.w " " crect.h
MsgBox geo_str: %geo_str%`ncrect_str: %crect_str%

Return
GetClientRect(hwnd) {
    VarSetCapacity(rc, 16)
    result := DllCall("GetClientRect", "PTR", hwnd, "PTR", &rc, "UINT")
    return {x : NumGet(rc, 0, "int")
    , y : NumGet(rc, 4, "int")
    , w : NumGet(rc, 8, "int")
    , h : NumGet(rc, 12, "int")}
}
