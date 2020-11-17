#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%
#Include, ../gdipbitmap.ahk
#Include, ../screen.ahk
#Include, ../window.ahk
; #Include, ../string.ahk
#Include, ../mdmf.ahk
#Include, ../ahk_functions.ahk

gdi_token := Gdip_Startup()
win_id := WinExist("A")

img_path := A_ScriptDir . "\test gdipbitmap from hwnd.png"
bitmap := gdipbitmap_from_handle(win_id)
gdipbitmap_to_file(bitmap, img_path)

; window_activate(hwnd)
; geo := window_get_geometry(win_id)
; bitmap := gdipbitmap_from_area(geo.x, geo.y, geo.w, geo.h)


Gdip_Shutdown(gdi_token)
