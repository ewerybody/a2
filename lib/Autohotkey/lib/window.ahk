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

window_toggle_maximize_width(win_id="") {
    win_id := _ensure_win_active(win_id)
    static memory := {}

	If !window_is_resizable(win_id)
		Return

    workarea := new Screen_WorkArea(screen_get_index(win_id))
	WinGetPos, wc_X, wc_Y, wc_Width, wc_Height, ahk_id %win_id%
	WinGet, wc_Max, MinMax, ahk_id %win_id%
	; maximize
	If (wc_Width <> workarea.width)
	{
        left := workarea.left
        right := workarea.width
		WinMove, ahk_id %win_id%,, %left%, %wc_Y%, % %right%, %wc_Height%
		; remember values for back toggling
		If (memory[win_id]["lastw"] <> wc_Width OR memory[win_id]["lasth"] <> wc_Height)
            memory[win_id] := {x: wc_X, y: wc_Y, w: wc_Width, h: wc_Height, minmax: wc_Max}
        memory[win_id]["lastw"] := workarea.width
        memory[win_id]["lasth"] := wc_Height
	}
    ; resest if remembered
	Else If (memory[win_id]["h"] <> "" AND memory[win_id]["w"] <> "")
	{
		If memory[win_id]["minmax"] = 1
			WinMaximize, ahk_id %win_id%
		Else
		{
			WinMove, A, , memory[win_id]["x"], memory[win_id]["y"], memory[win_id]["w"], memory[win_id]["h"]
            memory.Delete(win_id)
		}
	}
}

window_toggle_maximize_height(win_id="") {
    win_id := _ensure_win_active(win_id)
    static memory := {}

	If !window_is_resizable(win_id)
		Return

    workarea := new Screen_WorkArea(screen_get_index(win_id))
	WinGetPos, wc_X, wc_Y, wc_Width, wc_Height, ahk_id %win_id%
	WinGet, wc_Max, MinMax, ahk_id %win_id%
	; maximize
	If (wc_Height <> workarea.height)
	{
        top := workarea.top
        bottom := workarea.height
		WinMove, ahk_id %win_id%,, %wc_X%, %top%, % %wc_Width%, %bottom%
		; remember values for back toggling
		If (memory[win_id]["lastw"] <> wc_Width OR memory[win_id]["lasth"] <> wc_Height)
            memory[win_id] := {x: wc_X, y: wc_Y, w: wc_Width, h: wc_Height, minmax: wc_Max}
        memory[win_id]["lastw"] := wc_Width
        memory[win_id]["lasth"] := workarea.height
	}
    ; resest if remembered
	Else If (memory[win_id]["h"] <> "" AND memory[win_id]["w"] <> "")
	{
		If memory[win_id]["minmax"] = 1
			WinMaximize, ahk_id %win_id%
		Else
		{
			WinMove, A, , memory[win_id]["x"], memory[win_id]["y"], memory[win_id]["w"], memory[win_id]["h"]
            memory.Delete(win_id)
		}
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