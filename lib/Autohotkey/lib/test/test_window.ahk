WIN_FRAME_WIDTH := SysGet(32)
WIN_FRAME_HEIGHT := SysGet(33)
global WIN_FRAME_WIDTH
global WIN_FRAME_HEIGHT

#Include a2test.ahk
#Include %A_ScriptDir%\..\
; #Include  %A_ScriptDir%\..\..\..\a2_globals.ahk
#Include window.ahk
#Include screen.ahk

win_id := WinExist("A")

aot := window_is_aot(win_id)
window_set_aot(!aot, win_id)
aot2 := window_is_aot(win_id)

window_set_aot(aot, win_id)
aot3 := window_is_aot(win_id)
MsgBox("Setting Always-On-Top ON: " assertmsg(aot == !aot2) " OFF: " assertmsg(aot == aot3))
ahk_id := "ahk_id " . win_id
WinGetPos(&X, &Y, &Width, &Height, ahk_id)
window_get_rect(&_x, &_y, &_w, &_h, win_id)
msgbox("AHK xywh: " X "," Y "," Width "," Height "`nReal xywh: " _x "," _y "," _w "," _h "`nWIN_FRAME_WIDTH: " WIN_FRAME_WIDTH "`nWIN_FRAME_HEIGHT: " WIN_FRAME_HEIGHT)
test_size := [10, 10, 250, 340]
window_set_rect(test_size[1], test_size[2], test_size[3], test_size[4], win_id)
window_get_rect(&_x2, &_y2, &_w2, &_h2, win_id)
results := [_x2, _y2, _w2, _h2]
failed := false
for i, value in test_size {
    result := results[i]
    if (value != result) {
        failed := true
        msgbox("i: " . i . " value: " value ", result: " . result)
    }
}
msgbox("window_set_rect failed: " . failed)

if (!WinGetMinMax(ahk_id)) {
    msgbox("window_toggle_maximize ...")
    window_toggle_maximize()
}
msgbox("window_toggle_maximize ...")
window_toggle_maximize()

msgbox("window_toggle_maximize_width ...")
window_toggle_maximize_width()
msgbox("window_toggle_maximize_width ...")
window_toggle_maximize_width()

msgbox("window_toggle_maximize_height ...")
window_toggle_maximize_height()
msgbox("window_toggle_maximize_height ...")
window_toggle_maximize_height()

x := window_is_resizable()
if x
    msgbox("window_is_resizable! : " . x)
else
    msgbox("window_is NOT resizable! : " . x)

window_set_rect(_x, _y, _w, _h, win_id)
; window_toggle_maximize()
MsgBox("cutting a hole test ...")

geo := window_get_geometry(win_id)
geo_str := geo.x " " geo.y " " geo.w " " geo.h
border := 150
; rect := {x: geo.x + border, y: geo.y + border, x2: geo.w - border, y2: geo.h - border}
rect := {x: border, y: border, x2: geo.w - border, y2: geo.h - border}
rect_str := rect.x " " rect.y " " rect.w " " rect.h

window_cut_hole(win_id, rect)
msgbox("resetting ...")
WinSetRegion(, ahk_id)
window_set_rect(_x, _y, _w, _h, win_id)


win_list1 := window_list(0)
win_list2 := window_list(true)
msg := win_list1.Length " windows (" win_list2.Length " including hidden)`n"
explorers := []
for i, win in win_list1 {
    if (win_id == win.id) {
        msg .= i ' is active window: "' win.title '"`n  class: ' win.class "`n"
        msg .= "  hwnd: " win_id "`n  pid: " win.pid "`n  minmax: " win.minmax "`n"
        g := win.geo()
        msg .= "  xywh: " g.x " " g.y " " g.w " " g.h
    }
}

MsgBox(msg)
