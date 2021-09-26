; A ToolTip automatically following the mouse cursor
; https://www.autohotkey.com/docs/commands/ToolTip.htm
; when moved and disappearing by default.
; a2tip("help!")

a2tip(msg := "", timeout := "") {
    Global _a2tip_message, _a2_tip_id
    static last_timeout
    refresh_delay := 50

    _a2tip_message := msg

    if (timeout == "") {
        if (last_timeout != "")
            timeout := last_timeout
        else
            timeout := 1
    }

    if (timeout != 0) {
        ms_timeout := timeout * 1000
        SetTimer, a2tip_off, -%ms_timeout%
    }

    if not WinExist("ahk_id " _a2_tip_id)
    {
        tooltip,% (ttID:=msg) ;create tooltip and give it something to find it
        _a2_tip_id := WinExist(ttID ahk_class tooltips_class32) ;get ID from it
        font_set(_a2_tip_id, "s11, Arial")
        SetTimer, a2tip_timer, %refresh_delay%
    }

    a2tip_timer:
        CoordMode, Mouse, Screen
        MouseGetPos, mx_new, my_new
        ; if pos and text is the same, do not redraw
        if (mx_new == mx AND my_new == my AND msg == msg_old)
            return

        Tooltip, %_a2tip_message%
        mx := mx_new
        my := my_new
        msg_old := msg
    Return

    a2tip_off:
        _a2tip_message :=
        _a2_tip_id :=
        ToolTip
        SetTimer, a2tip_timer, Off
    Return
}

a2tip_add(msg, timeout := "") {
    Global _a2tip_message
    if (_a2tip_message)
        _a2tip_message .= "`n" msg
    else
        _a2tip_message := msg
    a2tip(_a2tip_message, timeout)
}
