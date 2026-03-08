#include <screen>

; Tell true/false 1/0 if the active or given window can be resized.
window_is_resizable(win_id:="") {
    if !win_id
        win_id := WinExist("A")

    style := WinGetStyle("ahk_id " win_id)
    if (style & 0x40000)
        return 1
    else
        return 0
}

; Maximize a floating window or restore a maximized one.
window_toggle_maximize(win_id:="") {
    win_id := _ensure_win_active(win_id)
    If !window_is_resizable(win_id)
        Return

    ahk_id := "ahk_id " win_id
    If (WinGetMinMax(ahk_id) == 1)
        WinRestore(ahk_id)
    Else
        WinMaximize(ahk_id)
}

; Maximize a window horizontally or restore its previous width.
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

    memory[win_id]["last_w"] := workarea.width
    memory[win_id]["last_h"] := wc_Height
}

; Maximize a window vertically or restore its previous height.
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

    memory[win_id]["last_w"] := wc_Width
    memory[win_id]["last_h"] := workarea.height
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
    If (!memory.has(win_id) OR (memory[win_id]["last_w"] !== wc_Width OR memory[win_id]["last_h"] !== wc_Height)) {
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

/**
 * Get a windows top-left position and dimensions into passed in arguments x, y, width, height.
 * @param {Integer} x
 * @param {Integer} y
 * @param {Integer} width
 * @param {Integer} height
 * @param {Integer} win_id
 */
window_get_rect(&x, &y, &width, &height, win_id := 0) {
    if (!win_id)
        win_id := WinExist("A")
    WinGetPos &_x, &_y, &_w, &_h, "ahk_id " . win_id
    x := _x + WIN_FRAME_WIDTH - 1
    y := _y
    width := _w - (WIN_FRAME_WIDTH - 1) * 2
    height := _h - (WIN_FRAME_HEIGHT - 1)
}

/**
 * Set a windows top-left position and dimensions from passed in arguments x, y, width, height.
 * @param {Integer} x
 * @param {Integer} y
 * @param {Integer} width
 * @param {Integer} height
 * @param {Integer} win_id
 */
window_set_rect(x, y, width, height, win_id := 0) {
    if (!win_id)
        win_id := WinExist("A")
    _x := x - WIN_FRAME_WIDTH + 1
    _w := width + (WIN_FRAME_WIDTH - 1) * 2
    _h := height + (WIN_FRAME_HEIGHT - 1)
    WinMove(_x, y, _w, _h, "ahk_id " . win_id)
}

/**
 * Set geo objects x,y,w,h,right,bottom values to the ones of given windows handle.
 * @param {Object} geo Geo object to be modified.
 * @param {Integer} hwnd Handle of window to get geometry data from.
 */
window_set_geo(&geo, hwnd) {
    window_get_rect(&x, &y, &w, &h, hwnd)
    geo.x := x, geo.y := y,
    geo.w := w, geo.h := h,
    geo.x2 := geo.x + geo.w
    geo.y2 := geo.y + geo.h
    geo.right := geo.x2
    geo.bottom := geo.y2
}

window_get_empty_geo() {
    return {x: 0, y: 0, x2: 0, y2: 0, right: 0, bottom: 0, w: 0, h: 0}
}


; Find a window's visible boundaries W10 compatible.
window_get_geometry(hwnd := 0) {
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

    r := {}
    r.x := NumGet(rect, 0, "Int"), r.y := NumGet(rect, 4, "Int")
    r.x2 := NumGet(rect, 8, "Int"), r.y2 := NumGet(rect, 12, "Int")
    r.right := r.x2, r.bottom := r.y2
    r.w := Abs(max(r.x, r.x2) - min(r.x, r.x2))
    r.h := Abs(max(r.y, r.y2) - min(r.y, r.y2))
    Return r
}

; Cut a rectangle into a window. But from rectangle-objects rather than this dash-galore-gobbledygook.
window_cut_hole(hwnd, inner, outer := "") {
    ; hwnd:     Window handle.
    ; inner:    Rectangle object with .x .y .x2 .y2 member attributes.
    ;           Where xy is the upper left and x2y2 the lower bottom corner.
    ;           Needs to be relative to the given window geometry as
    ;           WinSet, Region works RELATIVE to the window!
    ; outer:    Rectangle of the given window, or bigger. Just needs .w & .h.
    If (!IsObject(outer))
        outer := window_get_geometry(hwnd)
    outer_str := "0-0 " outer.w "-0 "
    outer_str .= outer.w "-" outer.h " 0-" outer.h " 0-0 "

    top_left2 := inner.x "-" inner.y
    inner_str := top_left2 " " inner.x2 "-" inner.y " "
    inner_str .= inner.x2 "-" inner.y2 " " inner.x "-" inner.y2 " " top_left2
    WinSetRegion(outer_str . inner_str, "ahk_id " . hwnd)
}

; Create list of window objects with range of information.
window_list(hidden:=0, process_name:="", class_name:="") {
    current_detect_state := A_DetectHiddenWindows
    if (current_detect_state != hidden) {
        DetectHiddenWindows(hidden)
    }

    windows := []
    n_windows := 0
    for win_id in WinGetList() {
        n_windows++
        ahk_id := "ahk_id " . win_id
        this_class := WinGetClass(ahk_id)
        if (class_name && this_class != class_name)
            continue

        try this_proc_name := WinGetProcessName(ahk_id)
        if !IsSet(this_proc_name)
            continue
        if (process_name && this_proc_name != process_name)
            continue

        title := WinGetTitle(ahk_id)
        min_max := WinGetMinMax(ahk_id)
        pid := WinGetPID(ahk_id)

        windows.push(_Window(this_proc_name, title, this_class, win_id, min_max, pid))
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

; Get a windows Always On Top state.
window_is_aot(win_id:="") {
    if !win_id
        win_id := WinExist("A")

    wc_ExStyle := WinGetExStyle("ahk_id " . win_id)
    if (wc_ExStyle & 0x8)
        return 1
    else
        return 0
}

; Set a windows Always On Top state.
window_set_aot(state, win_id := "") {
    if !win_id
        win_id := WinExist("A")

    WinSetAlwaysOnTop(state, "ahk_id " . win_id)
}

/**
 * Tell if a window extends to the borders of it's screen.
 * Works for maximized, F11 full-screen mode or just dragging the window big.
 * @param {Integer} [win_id] Optional. Handle of window to check. Default: Active Window.
 * @param {Screen_WorkArea} [screen_area] Optional. if already established: pass Screen_WorkArea
 * along to avoid recreating it over again.
 */
window_is_fullscreen(win_id := 0, screen_area := "") {
    if !win_id
        win_id := WinExist("A")

    if screen_area == ""
        screen_area := screen_get_work_area(screen_get_index(win_id))

    win_area := window_get_geometry(win_id)
    if win_area.x > screen_area.x
        return false
    if win_area.y > screen_area.y
        return false
    if win_area.x2 < screen_area.x2
        return false
    if win_area.y2 < screen_area.y2
        return false
    return true
}

/**
 * Move a window to the center of another window.
 * @param {Integer} this_hwnd Handle of a window to be centered.
 * @param {Integer} other_hwnd Handle of window to center the window on.
 */
window_set_center(this_hwnd, other_hwnd) {
    this_geo := window_get_geometry(this_hwnd)
    other_geo := window_get_geometry(other_hwnd)
    window_center_geo(&this_geo, &other_geo)
    WinMove(this_geo.x, this_geo.y,,, this_hwnd)
}

/**
 * Set a geo/rect object to be centered to another one.
 * @param this_geo
 * @param on_that_geo
 */
window_center_geo(&this_geo, on_that_geo) {
    center_x := on_that_geo.x + (on_that_geo.w / 2)
    center_y := on_that_geo.y + (on_that_geo.h / 2)
    this_geo.x := center_x - (this_geo.w / 2)
    this_geo.y := center_y - (this_geo.h / 2)
}

/**
 * Build string from rect object like window geo or ScreenWorkArea
 * @param rect
 */
window_format_geo(rect) {
    return "x: " rect.x " y: " rect.y " right: " rect.right " bottom: " rect.bottom " w: " rect.w " h: " rect.h
}
