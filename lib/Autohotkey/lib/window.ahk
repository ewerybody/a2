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

    ahk_id := "ahk_id " win_id

    If (WinGetMinMax(ahk_id) == 1)
        WinRestore(ahk_id)
    Else
    {
        WinMaximize(ahk_id)
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
    ; WinGetPos, wc_X, wc_Y, wc_Width, wc_Height, ahk_id %win_id%
    window_get_rect(wc_X, wc_Y, wc_Width, wc_Height, win_id)
    ; WinGet, wc_Max, MinMax, ahk_id %win_id%
    ; maximize
    If (wc_Width <> workarea.width)
    {
        ; left := workarea.left
        ; right := workarea.width
        ; WinMove, ahk_id %win_id%,, %left%, %wc_Y%, % %right%, %wc_Height%
        window_set_rect(workarea.left, wc_Y, workarea.width, wc_Height, win_id)
        ; remember values for back toggling
        If (memory[win_id]["lastw"] <> wc_Width OR memory[win_id]["lasth"] <> wc_Height)
            memory[win_id] := {x: wc_X, y: wc_Y, w: wc_Width, h: wc_Height, minmax: wc_Max}
        memory[win_id]["lastw"] := workarea.width
        memory[win_id]["lasth"] := wc_Height
    } Else
    _window_toggle_maximize_reset(win_id, memory)
}

window_toggle_maximize_height(win_id="") {
    win_id := _ensure_win_active(win_id)
    static memory := {}

    If !window_is_resizable(win_id)
        Return

    workarea := new Screen_WorkArea(screen_get_index(win_id))
    ; WinGetPos, wc_X, wc_Y, wc_Width, wc_Height, ahk_id %win_id%
    window_get_rect(wc_X, wc_Y, wc_Width, wc_Height, win_id)
    ; WinGet, wc_Max, MinMax, ahk_id %win_id%
    ; maximize
    If (wc_Height <> workarea.height)
    {
        top := workarea.top
        bottom := workarea.height
        ; WinMove, ahk_id %win_id%,, %wc_X%, %top%, % %wc_Width%, %bottom%
        window_set_rect(wc_X, top, wc_Width, bottom, win_id)
        ; remember values for back toggling
        If (memory[win_id]["lastw"] <> wc_Width OR memory[win_id]["lasth"] <> wc_Height)
            memory[win_id] := {x: wc_X, y: wc_Y, w: wc_Width, h: wc_Height, minmax: wc_Max}
        memory[win_id]["lastw"] := wc_Width
        memory[win_id]["lasth"] := workarea.height
    } Else
    _window_toggle_maximize_reset(win_id, memory)
}

_window_toggle_maximize_reset(byref win_id, byref memory) {
    If (memory[win_id]["h"] <> "" AND memory[win_id]["w"] <> "")
    {
        If memory[win_id]["minmax"] = 1
            WinMaximize, ahk_id %win_id%
        Else
        {
            window_set_rect(memory[win_id]["x"], memory[win_id]["y"], memory[win_id]["w"], memory[win_id]["h"], win_id)
            memory.Delete(win_id)
        }
    }
}

window_activate(win_id, seconds := 5) {
    ; Make sure a window with hwnd `win_id` is activated.
    ; Activate it if needed, wait for `seconds`.
    ; To wait forever set `seconds` to 0.
    IfWinNotActive, ahk_id %win_id%
    {
        WinActivate, ahk_id %win_id%
        if (seconds)
            WinWaitActive, ahk_id %win_id%,, %seconds%
        else
            WinWaitActive, ahk_id %win_id%,
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

window_get_rect(byref x, byref y, byref width, byref height, win_id="") {
    if (!win_id)
        win_id := WinExist("A")
    WinGetPos, _x, _y, _w, _h, ahk_id %win_id%
    x := _x + WIN_FRAME_WIDTH - 1
    y := _y
    width := _w - (WIN_FRAME_WIDTH - 1) * 2
    height := _h - (WIN_FRAME_HEIGHT - 1)

    ; txt = _x:%_x%, x: %x%, WIN_FRAME_WIDTH: %WIN_FRAME_WIDTH%`n_y:%_y%,y: %y%, WIN_FRAME_HEIGHT: %WIN_FRAME_HEIGHT%,`n_w:%_w%, width: %width%, _h:%_h%, height: %height%
}

window_set_rect(byref x, byref y, byref width, byref height, win_id="") {
    if (!win_id)
        win_id := WinExist("A")
    _x := x - WIN_FRAME_WIDTH + 1
    _w := width + (WIN_FRAME_WIDTH - 1) * 2
    _h := height + (WIN_FRAME_HEIGHT - 1)

    ; txt = _x:%_x%, x: %x%, WIN_FRAME_WIDTH: %WIN_FRAME_WIDTH%`n_y:%_y%,y: %y%,
    ; txt = %txt% WIN_FRAME_HEIGHT: %WIN_FRAME_HEIGHT%,`n_w:%_w%, width: %width%, _h:%_h%, height: %height%
    WinMove, ahk_id %win_id%,, %_x%, %y%, %_w%, %_h%
}

window_get_geometry(hwnd) {
    ; Find a window's visible boundaries W10 compatible.
    ; From GeekDude:
    ; https://gist.github.com/G33kDude/5b7ba418e685e52c3e6507e5c6972959#file-volume-ahk-L85
    ; Modified by Marius Șucan to return an array where:
    ; geo := window_get_geometry(handle)
    ; geo.x, geo.y   : Top-left corner of the window
    ; geo.w, geo.h   : Extends of the window in width & height
    ; geo.x2, geo.y2   : Bottom-right corner of the window
    size := VarSetCapacity(rect, 16, 0)
    error := DllCall("dwmapi\DwmGetWindowAttribute"
    , "UPtr", hWnd ; HWND  hwnd
    , "UInt", 9 ; DWORD dwAttribute (DWMWA_EXTENDED_FRAME_BOUNDS)
    , "UPtr", &rect ; PVOID pvAttribute
    , "UInt", size ; DWORD cbAttribute
    , "UInt") ; HRESULT

    If error {
        DllCall("GetWindowRect", "UPtr", hwnd, "UPtr", &rect, "UInt")
    }

    r := []
    r.x := NumGet(rect, 0, "Int"), r.y := NumGet(rect, 4, "Int")
    r.x2 := NumGet(rect, 8, "Int"), r.y2 := NumGet(rect, 12, "Int")
    r.w := Abs(max(r.x, r.x2) - min(r.x, r.x2))
    r.h := Abs(max(r.y, r.y2) - min(r.y, r.y2))
    Return r
}

window_cut_hole(hwnd, inner, outer := "") {
    ; Cut a rectangle into a window. But from rectangle-object
    ; rather than this huge coordinates string.
    ;
    ; hwnd:     Window handle.
    ; inner:    Rectangle object with .x .y .x2 .y2 member attributes.
    ;           Where xy is the upper left and x2y2 the lower bottom corner.
    ;           Needs to be relative to the given window geometry as
    ;           WinSet, Region works RELATIVE to the window!
    ; outer:    Rectangle of the given window, or bigger. Just needs .w & .h.
    If (!IsObject(outer))
        outer := window_get_geometry(hwnd)
    outer_str := "0-0 " outer.w "-0 "
    outer_str .= outer.w "-" outer.h " 0-" outer.h " 0-0"

    top_left2 := inner.x "-" inner.y
    inner_str := top_left2 " " inner.x2 "-" inner.y " "
    inner_str .= inner.x2 "-" inner.y2 " " inner.x "-" inner.y2 " " top_left2
    ; a2tip(hwnd "`n" outer_str "`n" inner_str "`nx:" inner.x "`ny:" inner.y "`nx2:" inner.x2 "`ny2:" inner.y2)
    WinSet, Region, %outer_str% %inner_str%, ahk_id %hwnd%
}

window_list(hidden=0, process_name="", class_name="") {
    ; Create list of window objects with range of information.
    current_detect_state := DetectHiddenWindows()
    if (current_detect_state != hidden) {
        DetectHiddenWindows(hidden)
    }

    windows := []
    WinGet, win_ids, list
    loop %win_ids% {
        winid := win_ids%A_Index%
        ahkid := "ahk_id " winid
        WinGet, proc, ProcessName, %ahkid%
        if (process_name && proc != process_name)
            continue

        WinGetClass, clss, %ahkid%
        if (class_name && clss != class_name)
            continue

        WinGetTitle, title, %ahkid%
        WinGet, min_max, MinMax, %ahkid%
        WinGet, pid, PID, %ahkid%

        windows.push(new _Window(proc, title, clss, winid, min_max, pid))
    }

    if (current_detect_state != hidden)
        DetectHiddenWindows(current_detect_state)

    return windows
}

class _Window {
    ; Abstract window information object.
    __New(proc_name, win_title, win_class, id, minmax, pid) {
        this.proc_name := proc_name
        this.title := win_title
        this.class := win_class
        this.id := id
        this.minmax := minmax
        this.pid := pid
    }

    geo() {
        return window_get_geometry(this.id)
    }
}
