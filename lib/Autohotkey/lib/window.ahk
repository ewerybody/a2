window_is_resizable(win_id="") {
    if !win_id
        win_id := WinExist("A")

    style := WinGetStyle("ahk_id " win_id)
    if (style & 0x40000)
        return 1
    else
        return 0
}

window_toggle_maximize(win_id="") {
    win_id := _ensure_win_active(win_id)
    
	If !window_is_resizable(win_id)
		Return

	If (WinGetMinMax("A") == 1)
		WinRestore("A")
	Else
	{
		WinMaximize("A")
        ; I don't know why that was implemented. seems unnecessary.
        ; workarea := new Screen_WorkArea(screen_get_index(win_id))
        ; x := workarea.left
        ; y := workarea.top
        ; w := workarea.width
        ; h := workarea.height
		; WinMove, ahk_id %win_id%, , %x%, %y%, %w%, %h%
	}
}

window_activate(win_id) {
    IfWinNotActive, ahk_id %win_id%
    {
        WinActivate, ahk_id %win_id%
        WinWaitActive, ahk_id %win_id%
    }
}

window_activate_on_mouse_input() {
	If A_ThisHotkey contains MButton,LButton,RButton,XButton1,XButton2
	{
		MouseGetPos,,, win_id
        window_activate(win_id)
        return win_id
	}
}

_ensure_win_active(win_id) {
    if !win_id
    {
        win_id := window_activate_on_mouse_input()
        if !win_id
            win_id := WinExist("A")
    }
    else
        window_activate(win_id)
    return win_id
}