#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%
#Include, ../gdipbitmap.ahk
#Include, ../gdip.ahk
#Include, ../screen.ahk
#Include, ../window.ahk
#Include, ../string.ahk
#Include, ../mdmf.ahk
#Include, ../ahk_functions.ahk

gdi_token := gdip_startup()
win_id := WinExist("A")

; img_path := A_ScriptDir . "\test gdipbitmap from hwnd.png"
; bitmap := gdipbitmap_from_handle(win_id)
; bitmap := gdipbitmap_from_screen()

; window_activate(hwnd)
img_path := A_ScriptDir . "\test gdipbitmap from area.png"
geo := window_get_geometry(win_id)
; bitmap := gdipbitmap_from_area(geo.x, geo.y, geo.w, geo.h)

coords := string_join([geo.x, geo.y, geo.w, geo.h], "|")
bitmap := gdipbitmap_from_coords_string(coords)

gdipbitmap_to_file(bitmap, img_path)

gdip_shutdown(gdi_token)
