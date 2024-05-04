#Requires AutoHotkey v2.0
#include <window>
WIN_FRAME_WIDTH := SysGet(32)
WIN_FRAME_HEIGHT := SysGet(33)
global WIN_FRAME_WIDTH
global WIN_FRAME_HEIGHT

win_id := WinExist("A")
ahk_id := "ahk_id " win_id
window_get_rect(&_x, &_y, &_w, &_h, win_id)
MsgBox("cutting a hole test ...")

geo := window_get_geometry(win_id)
geo_str := geo.x " " geo.y " " geo.w " " geo.h
border := 150
; rect := {x: geo.x + border, y: geo.y + border, x2: geo.w - border, y2: geo.h - border}
rect := {x: border, y: border, x2: geo.w - border, y2: geo.h - border}
rect_str := rect.x " " rect.y " " rect.x2 " " rect.y2

WinSetTransparent(200, ahk_id)
window_cut_hole(win_id, rect)
msgbox("resetting ...")
WinSetRegion(, ahk_id)
window_set_rect(_x, _y, _w, _h, win_id)
WinSetTransparent("Off", ahk_id)