SysGet, WIN_FRAME_WIDTH, 32
SysGet, WIN_FRAME_HEIGHT, 33
global WIN_FRAME_WIDTH
global WIN_FRAME_HEIGHT

#Include  %A_ScriptDir%\..\ahk_functions.ahk
; #Include  %A_ScriptDir%\..\..\..\a2_globals.ahk
#Include  %A_ScriptDir%\..\window.ahk
#Include  %A_ScriptDir%\..\screen.ahk

win_id := WinExist("A")
WinGetPos, X, Y, Width, Height, ahk_id %win_id%
window_get_rect(_x, _y, _w, _h, win_id)
msgbox AHK xywh: %X%,%Y%,%Width%,%Height%`nReal xywh: %_x%,%_y%,%_w%,%_h%`nWIN_FRAME_WIDTH: %WIN_FRAME_WIDTH%`nWIN_FRAME_HEIGHT: %WIN_FRAME_HEIGHT%
test_size := [10, 10, 250, 340]
window_set_rect(test_size[1], test_size[2], test_size[3], test_size[4], win_id)
window_get_rect(_x2, _y2, _w2, _h2, win_id)
results := [_x2, _y2, _w2, _h2]
failed := false
for i, value in test_size {
    result := results[i]
    if (value != result) {
        failed := true
        msgbox i: %i% value: %value%, result: %result%
    }
}
msgbox window_set_rect failed: %failed%

msgbox window_toggle_maximize ...
window_toggle_maximize()
msgbox window_toggle_maximize ...
window_toggle_maximize()

msgbox window_toggle_maximize_width ...
window_toggle_maximize_width()
msgbox window_toggle_maximize_width ...
window_toggle_maximize_width()

msgbox window_toggle_maximize_height ...
window_toggle_maximize_height()
msgbox window_toggle_maximize_height ...
window_toggle_maximize_height()

x := window_is_resizable()
if x
    msgbox window_is_resizable! : %x%
else
    msgbox window_is NOT resizable! : %x%
window_set_rect(_x, _y, _w, _h, win_id)
