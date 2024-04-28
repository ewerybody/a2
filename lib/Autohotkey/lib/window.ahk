#include <screen>

window_is_resizable(win_id:="") {
    if !win_id
        win_id := WinExist("A")

    style := WinGetStyle("ahk_id " win_id)
    if (style & 0x40000)
        return 1
    else
        return 0
}

window_toggle_maximize(win_id:="") {
    win_id := _ensure_win_active(win_id)

    If !window_is_resizable(win_id)
        Return

    ahk_id := "ahk_id " win_id

    If (WinGetMinMax(ahk_id) == 1) {
        WinRestore(ahk_id)
    }
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

window_toggle_maximize_width(win_id:="") {
    win_id := _ensure_win_active(win_id)
    If !window_is_resizable(win_id)
        Return

    static memory := Map()

    workarea := Screen_WorkArea(screen_get_index(win_id))
    window_get_rect(&wc_X, &wc_Y, &wc_Width, &wc_Height, win_id)
    wc_Max := WinGetMinMax("ahk_id " . win_id)
    If (wc_Width == workarea.width) {
        _window_toggle_maximize_reset(win_id, &memory)
        Return
    }

    window_set_rect(workarea.left, wc_Y, workarea.width, wc_Height, win_id)
    _window_toggle_maximize_set_mem(&memory, win_id, wc_Width, wc_Height, wc_X, wc_Y, wc_Max)

    memory[win_id]["lastw"] := workarea.width
    memory[win_id]["lasth"] := wc_Height
}

window_toggle_maximize_height(win_id:="") {
    win_id := _ensure_win_active(win_id)
    If !window_is_resizable(win_id)
        Return

    static memory := Map()
    workarea := Screen_WorkArea(screen_get_index(win_id))
    window_get_rect(&wc_X, &wc_Y, &wc_Width, &wc_Height, win_id)
    wc_Max := WinGetMinMax("ahk_id " . win_id)
    If (wc_Height == workarea.height) {
        _window_toggle_maximize_reset(win_id, &memory)
        Return
    }

    window_set_rect(wc_X, workarea.top, wc_Width, workarea.height, win_id)
    _window_toggle_maximize_set_mem(&memory, win_id, wc_Width, wc_Height, wc_X, wc_Y, wc_Max)

    memory[win_id]["lastw"] := wc_Width
    memory[win_id]["lasth"] := workarea.height
}

_window_toggle_maximize_reset(win_id, &memory) {
    If (memory[win_id]["h"] !== "" AND memory[win_id]["w"] !== "")
    {
        If memory[win_id]["minmax"] = 1
            WinMaximize("ahk_id " . win_id)
        Else
        {
            window_set_rect(memory[win_id]["x"], memory[win_id]["y"], memory[win_id]["w"], memory[win_id]["h"], win_id)
            memory.Delete(win_id)
        }
    }
}

; remember values for back toggling
_window_toggle_maximize_set_mem(&memory, win_id, wc_Width, wc_Height, wc_X, wc_Y, wc_Max) {
    If (!memory.has(win_id) OR (memory[win_id]["lastw"] !== wc_Width OR memory[win_id]["lasth"] !== wc_Height)) {
        memory[win_id] := Map("x", wc_X, "y", wc_Y, "w", wc_Width, "h", wc_Height, "minmax", wc_Max)
    }
}

; Make sure a window with hwnd `win_id` is activated.
; Activate it if needed, wait for `seconds`.
; To wait forever set `seconds` to 0.
window_activate(win_id, seconds := 5) {
    ahk_id := "ahk_id " win_id
    If !WinActive(ahk_id)
    {
        WinActivate(ahk_id)
        if (seconds)
            WinWaitActive(ahk_id,,seconds)
        else
            WinWaitActive(ahk_id)
    }
}

window_activate_on_mouse_input() {
    buttons := 'MButton,LButton,RButton,XButton1,XButton2'
    Loop parse, buttons, ","
    {
        If (A_ThisHotkey = A_LoopField)
        {
            MouseGetPos , , &win_id
            window_activate(win_id)
            return win_id
        }
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

window_get_rect(&x, &y, &width, &height, win_id:="") {
    if (!win_id)
        win_id := WinExist("A")
    WinGetPos &_x, &_y, &_w, &_h, "ahk_id " . win_id
    x := _x + WIN_FRAME_WIDTH - 1
    y := _y
    width := _w - (WIN_FRAME_WIDTH - 1) * 2
    height := _h - (WIN_FRAME_HEIGHT - 1)

    ; txt = _x:%_x%, x: %x%, WIN_FRAME_WIDTH: %WIN_FRAME_WIDTH%`n_y:%_y%,y: %y%, WIN_FRAME_HEIGHT: %WIN_FRAME_HEIGHT%,`n_w:%_w%, width: %width%, _h:%_h%, height: %height%
}

window_set_rect(x, y, width, height, win_id:="") {
    if (!win_id)
        win_id := WinExist("A")
    _x := x - WIN_FRAME_WIDTH + 1
    _w := width + (WIN_FRAME_WIDTH - 1) * 2
    _h := height + (WIN_FRAME_HEIGHT - 1)

    ; txt = _x:%_x%, x: %x%, WIN_FRAME_WIDTH: %WIN_FRAME_WIDTH%`n_y:%_y%,y: %y%,
    ; txt = %txt% WIN_FRAME_HEIGHT: %WIN_FRAME_HEIGHT%,`n_w:%_w%, width: %width%, _h:%_h%, height: %height%
    WinMove(_x, y, _w, _h, "ahk_id " . win_id)
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
    ; size := VarSetCapacity(&rect, 16, 0)
    size := Buffer(16)
    ; size := Number(16)
    rect := Buffer(24, 0)
    error := DllCall("dwmapi\DwmGetWindowAttribute"
        , "UPtr", hWnd ; HWND  hwnd
        , "UInt", 9 ; DWORD dwAttribute (DWMWA_EXTENDED_FRAME_BOUNDS)
        , "Ptr", rect ; PVOID pvAttribute
        , "UInt", 16 ; DWORD cbAttribute
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
    WinSetRegion(outer_str . inner_str, "ahk_id " . hwnd)
}

; Create list of window objects with range of information.
window_list(hidden:=0, process_name:="", class_name:="") {
    current_detect_state := A_DetectHiddenWindows
    if (current_detect_state != hidden) {
        DetectHiddenWindows(hidden)
    }

    windows := []
    for win_id in WinGetlist() {
        ahkid := "ahk_id " . win_id
        clss := WinGetClass(ahkid)
        if (class_name && clss != class_name)
            continue

        proc := WinGetProcessName(ahkid)
        if (process_name && proc != process_name)
            continue

        title := WinGetTitle(ahkid)
        min_max := WinGetMinMax(ahkid)
        pid := WinGetPID(ahkid)

        windows.push(_Window(proc, title, clss, win_id, min_max, pid))
    }

    if (current_detect_state != hidden)
        DetectHiddenWindows(current_detect_state)

    return windows
}

; Abstract window information object.
class _Window {
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

window_is_aot(win_id:="") {
    ; Get a windows Always On Top state.
    if !win_id
        win_id := WinExist("A")

    wc_ExStyle := WinGetExStyle("ahk_id " . win_id)
    if (wc_ExStyle & 0x8)
        return 1
    else
        return 0
}

window_set_aot(state, win_id := "") {
    ; Set a windows Always On Top state.
    if !win_id
        win_id := WinExist("A")

    WinSetAlwaysOnTop(state, "ahk_id " . win_id)
}
