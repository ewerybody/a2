; Screen dimming overlay gui
; fades in and out smoothly

dimmer_create(area := "") {
    global _screen_dimmer_alpha, _screen_dimmer_id
    _screen_dimmer_alpha := 128

    Gui, New , +AlwaysOnTop -Caption -Border +ToolWindow -Resize +Disabled -DPIScale, ScreenDimmerGui
    Gui, +LastFound
    WinGet, new_id, ID
    Gui, Color, 000000
    WinSet, Transparent, 0

    if (new_id != _screen_dimmer_id) AND WinExist("ahk_id " _screen_dimmer_id) {
        WinClose, ahk_id %_screen_dimmer_id%
    }
    _screen_dimmer_id := new_id

    if (!IsObject(area)) {
        area := screen_get_work_area()
    }
    area_str := "x" area.left " y" area.top " w" area.w " h" area.h
    Gui, Show, %area_str%, ScreenDimmerGui
    SetTimer, _dimmer_turn_up, 25
    return _screen_dimmer_id
}

_dimmer_turn_up() {
    global _screen_dimmer_alpha, _screen_dimmer_id

    WinGet, value, Transparent, ahk_id %_screen_dimmer_id%
    value += 20
    if (value > _screen_dimmer_alpha) {
        SetTimer, _dimmer_turn_up, Off
        return
    }

    WinSet, Transparent, %value%, ahk_id %_screen_dimmer_id%
}

dimmer_off(finished_func := "") {
    SetTimer, _dimmer_turn_down, 25
    global _screen_dimmer_finished_func
    if IsFunc(finished_func)
        _screen_dimmer_finished_func := finished_func
}

_dimmer_turn_down() {
    global _screen_dimmer_id, _screen_dimmer_finished_func
    id_str := "ahk_id " _screen_dimmer_id
    if (!WinExist(id_str)) {
        SetTimer, _dimmer_turn_down, Off
        return
    }
    WinGet, value, Transparent,
    value -= 20
    if (value < 0) {
        SetTimer, _dimmer_turn_down, Off
        WinHide, %id_str%
        if IsFunc(_screen_dimmer_finished_func)
            %_screen_dimmer_finished_func%()
        return
    }

    WinSet, Transparent, %value%, %id_str%
}
