; A simple mouse cursor following, self removing ToolTip.
; https://www.autohotkey.com/docs/commands/ToolTip.htm
; a2tip("Hello, World!")

; TODO: repair the font stuff
; #include font.ahk

a2tip(msg := "", timeout := "") {
    Global _a2tip_message := ""
    Global _a2tip_id := 0, a2tip_refresh, a2tip_offset_x, a2tip_offset_y
    estimate_s_per_char := 20
    estimate_min := 1
    estimate_max := 10

    if !msg {
        ToolTip("")
        Return
    }

    if (timeout == "") {
        timeout := Min(estimate_max, Max(estimate_min, StrLen(msg) / estimate_s_per_char))
    } else if timeout <= 0 {
        ToolTip("")
        Return
    }
    timeout *= 1000
    SetTimer(_a2tip_off, -timeout)

    if !IsSet(a2tip_refresh)
        a2tip_refresh := 50

    if !IsSet(a2tip_offset_x)
        a2tip_offset_x := 30
    if !IsSet(a2tip_offset_y)
        a2tip_offset_y := 0

    _a2tip_message := msg

    if (!WinExist("ahk_id " _a2tip_id)) {
        _a2tip_id := _a2tip_draw()
        ; font_set(_a2tip_id, "s11, Arial")
        SetTimer(_a2tip_draw, a2tip_refresh)
    }
}

_a2tip_draw() {
    Global _a2tip_id
    CoordMode "Mouse", "Screen"
    MouseGetPos &mx_new, &my_new
    Static mx := 0, my := 0
    Static msg_old := ""
    ; if pos and text is the same, do not redraw
    if (mx_new == mx AND my_new == my AND _a2tip_message == msg_old)
        return

    if _a2tip_id == 0 {
        SetTimer(_a2tip_draw, 0)
        Return
    }

    ; Since AHK2.0 we now have the direct tooltip handle and could use `WinMove`
    ; to not redraw the tooltip and "just" move it! But there are multiple
    ; drawbacks: 1st: It actually seems to be slower!, 2nd: WinMove makes the
    ; tooltip in-transparent to clicks and thus prevents click-through.
    CoordMode "ToolTip", "Screen"
    _a2tip_id := ToolTip(_a2tip_message, mx_new + a2tip_offset_x, my_new + a2tip_offset_y)

    ; coloring the tooltip is a loosing battle .. we probably need a custom tooltip then :)
    ; DllCall("uxtheme\SetWindowTheme", "Ptr", _a2tip_id, "Str", "", "Str", "")
    ; SendMessage(0x1013, 0xFFFF00, 0, , "ahk_id " _a2tip_id)  ; TTM_SETTIPBKCOLOR
    ; SendMessage(0x1014, 0x00FFFF, 0, , "ahk_id " _a2tip_id)  ; TTM_SETTIPTEXTCOLOR

    mx := mx_new, my := my_new
    msg_old := _a2tip_message
    Return _a2tip_id
}

_a2tip_off() {
    SetTimer(_a2tip_draw, 0)
    if WinExist("ahk_id " . _a2tip_id)
        WinClose("ahk_id " . _a2tip_id)
}

a2tip_add(msg, timeout := "") {
    if (_a2tip_message)
        _a2tip_message .= "`n" msg
    else
        _a2tip_message := msg

    a2tip(_a2tip_message, timeout)
}
