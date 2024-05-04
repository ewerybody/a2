; Screen dimming overlay gui
; fades in and out smoothly

dimmer_create(area := "") {
    global _screen_dimmer_alpha, _screen_dimmer_id
    _screen_dimmer_alpha := 128

    dimmer_gui := Gui("+AlwaysOnTop -Caption -Border +ToolWindow -Resize +Disabled -DPIScale +LastFound")
    ; Gui, New , +AlwaysOnTop -Caption -Border +ToolWindow -Resize +Disabled -DPIScale, ScreenDimmerGui
    ; Gui, +LastFound
    ; new_id := WinGetID
    dimmer_gui.BackColor := "000000"
    try {
        if (dimmer_gui.Hwnd != _screen_dimmer_id) AND WinExist("ahk_id " _screen_dimmer_id)
            WinClose("ahk_id " _screen_dimmer_id)
    }
    _screen_dimmer_id := dimmer_gui.Hwnd

    if (!IsObject(area)) {
        area := screen_get_work_area()
    }
    dimmer_gui.Show("x" area.left " y" area.top " w" area.w " h" area.h)
    WinSetTransparent(0, "ahk_id " dimmer_gui.Hwnd)
    SetTimer _dimmer_turn_up, 25
    return _screen_dimmer_id
}

_dimmer_turn_up() {
    global _screen_dimmer_alpha, _screen_dimmer_id

    value := WinGetTransparent("ahk_id " _screen_dimmer_id)
    value += 20
    if (value > _screen_dimmer_alpha) {
        SetTimer _dimmer_turn_up, 0
        return
    }

    WinSetTransparent(value, "ahk_id " _screen_dimmer_id)
}

dimmer_off(finished_func := "") {
    SetTimer _dimmer_turn_down, 25
    global _screen_dimmer_finished_func
    if IsObject(finished_func)
        _screen_dimmer_finished_func := finished_func
}

_dimmer_turn_down() {
    global _screen_dimmer_id, _screen_dimmer_finished_func
    id_str := "ahk_id " _screen_dimmer_id
    if (!WinExist(id_str)) {
        SetTimer _dimmer_turn_down, 0
        return
    }
    value := WinGetTransparent(id_str)
    value -= 20
    if (value < 0) {
        SetTimer _dimmer_turn_down, 0
        WinHide(id_str)
        try {
            if IsObject(_screen_dimmer_finished_func)
                %_screen_dimmer_finished_func%()
        }
        return
    }

    WinSetTransparent(value, id_str)
}
