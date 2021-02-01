dimmer_id := dimmer_create()
m1 := assertmsg(dimmer_id)
MsgBox % m1 " Created dimmer gui hwnd: " dimmer_id
dimmer_off()

area := screen_get_work_area()
area.w := Floor(area.w /2)
MsgBox % "area:`nx:" area.x " y:" area.y " w:" area.w " h:" area.h
dimmer_id := dimmer_create(area)
MsgBox % m1 " Created half a dimmer gui hwnd: " dimmer_id
dimmer_off("_test_dimmer_exit")

Return
#SingleInstance, force
#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include dimmer.ahk
#Include screen.ahk

_test_dimmer_exit() {
    ExitApp
}