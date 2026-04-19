; A simple mouse cursor following, self removing ToolTip.
; https://www.autohotkey.com/docs/commands/ToolTip.htm
; a2tip("Hello, World!")
#Include <font>

/**
 * Create a mouse-following little message tooltip.
 * @param {(String)} [msg] - Message to be displayed by tooltip. (Default: "" makes last tooltip disappear)
 * @param {(Integer)} [timeout] - Seconds to show the tooltip. Available options are:
 * X - A Number of seconds. Tooltip disappears afterwards.
 * "" - Default. nothing set: Enables timeout estimation by length of message.
 * -1 - "Forever" keep the tooltip displayed.
 * @param {(String)} [font] - String for font change. E.g. `s15, Comic Sans MS`.
 */
a2tip(msg := "", timeout := "", font := "") {
    Global a2tip_message := ""
    Global _a2tip_id := 0, a2tip_refresh, a2tip_offset_x, a2tip_offset_y, a2tip_font
    estimate_s_per_char := 20
    estimate_min := 1
    estimate_max := 10

    a2tip_font := font ? font : ""
    if !msg {
        ToolTip("")
        Return
    }

    if (timeout == "") {
        timeout := Min(estimate_max, Max(estimate_min, StrLen(msg) / estimate_s_per_char))
    } else if timeout == 0 {
        ToolTip("")
        Return
    } else if timeout == -1 {
        ; "Forever" is like 5min for now ;)
        timeout := 300
    }
    timeout *= 1000
    SetTimer(_a2tip_off, -timeout)

    if !IsSet(a2tip_refresh)
        a2tip_refresh := 50

    if !IsSet(a2tip_offset_x)
        a2tip_offset_x := 30
    if !IsSet(a2tip_offset_y)
        a2tip_offset_y := 0

    a2tip_message := msg

    if (!WinExist("ahk_id " _a2tip_id)) {
        _a2tip_id := _a2tip_draw()
        SetTimer(_a2tip_draw, a2tip_refresh)
    }
}

a2tip_add(msg, timeout := "") {
    if (a2tip_message)
        a2tip_message .= "`n" msg
    else
        a2tip_message := msg

    a2tip(a2tip_message, timeout)
}


_a2tip_draw() {
    Global _a2tip_id
    CoordMode "Mouse", "Screen"
    MouseGetPos &mx_new, &my_new
    Static mx := 0, my := 0, msg_old := "", last_tip_id := 0, num_draws := 2
    ; if pos and text is the same, do not redraw
    if (num_draws == 0 AND mx_new == mx AND my_new == my AND a2tip_message == msg_old)
        return _a2tip_id

    ; Since AHK2.0 we now have the direct tooltip handle and could use `WinMove`
    ; to not redraw the tooltip and "just" move it! But there are multiple
    ; drawbacks: 1st: It actually seems to be slower!, 2nd: WinMove makes the
    ; tooltip in-transparent to clicks and thus prevents click-through.
    CoordMode "ToolTip", "Screen"
    _a2tip_id := ToolTip(a2tip_message, mx_new + a2tip_offset_x, my_new + a2tip_offset_y)
    if a2tip_font AND last_tip_id != _a2tip_id && _a2tip_id != 0 {
        font_set(_a2tip_id, a2tip_font)
        last_tip_id := _a2tip_id
        num_draws := 2
    }
    num_draws -= 1

    ; coloring the tooltip is a loosing battle .. we probably need a custom tooltip then :)
    ; DllCall("uxtheme\SetWindowTheme", "Ptr", _a2tip_id, "Str", "", "Str", "")
    ; SendMessage(0x1013, 0xFF0F0F, 0, , "ahk_id " _a2tip_id)  ; TTM_SETTIPBKCOLOR
    ; SendMessage(0x1014, 0x0000FF, 0, , "ahk_id " _a2tip_id)  ; TTM_SETTIPTEXTCOLOR

    mx := mx_new, my := my_new
    msg_old := a2tip_message
    Return _a2tip_id
}

_a2tip_off() {
    global _a2tip_id
    SetTimer(_a2tip_draw, 0)
    if WinExist("ahk_id " _a2tip_id)
        WinClose("ahk_id " _a2tip_id)
    _a2tip_id := 0
}
