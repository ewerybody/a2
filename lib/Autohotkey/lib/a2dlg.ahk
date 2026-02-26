/************************************************************************
 * a2dlg.ahk — reusable dialog helpers for a2
 *
 * Low-level (function-based):
 *  a2dlg_make_button(ctrl, bg, fg)              — owner-drawn button with custom colors
 *  a2dlg_is_dark()                       — true when Windows dark mode is active
 *  a2dlg_colors(dark)                    — standard a2 color scheme object
 *  a2dlg_apply_dark_title_bar(hwnd, dark) — DWM dark/light title bar
 * High-level (A2Dialog class):
 *   d := A2Dialog(title [, opts])            — opts: w, pad, flags, dark, font: {face, size}
 *   d.header(text [, icon_path])             — large title with optional 32px icon
 *   d.sep()                                  — thin horizontal separator line
 *   d.row(icon, color, text [, subtext])     — colored icon + label row → {icon, text}
 *   d.row_pending([icon, text])              — muted row for live update → {icon, text}
 *   d.text(content [, ahk_opts])             — small caption / status line → ctrl
 *   d.space(px)                              — extra vertical gap
 *   d.btn(label, bg, fg [, ahk_opts])        — single flat button → ctrl
 *   d.btn_row(specs [, h, gap, bw])          — left-aligned button row → [controls]
 *   d.btn_row_right(specs [, bw, h, gap])    — right-aligned footer row → [controls]
 *   d.show([extra_h])                        — first show, centered on screen
 *   d.resize([extra_h])                      — resize in-place (progressive reveal)
 *   d.set_icon(path)                         — set window title-bar / taskbar icon
 *   d.esc_to_close([fn])                     — Esc closes or calls fn
 *   d.on_close(fn)                           — register Gui Close handler
 *   d.destroy()                              — destroy window and clean up btn registry
 *   d.gui  d.hwnd  d.c  d.dark              — direct access to underlying objects
 *  Button specs (for btn_row / btn_row_right): array of {label, bg, fg [, opts]}
 *    opts: extra AHK button option string, e.g. "Default"
 *  Color strings are always 6-digit "RRGGBB" hex (no #).
 *  Include this file once per script — it self-registers the WM_DRAWITEM handler.
  ***********************************************************************/

/**
 * A2Dialog — composable dialog builder
 */
class A2Dialog {
    ; Layout state
    gui := ""
    dark := false
    c := {}
    _w := 480
    _pad := 14
    _y := 0
    _face := "Segoe UI"
    _fsz := 10            ; base font size — all other sizes derived from this
    _btn_hwnds := []            ; tracked for cleanup in destroy()
    _destroyed := false         ; guard against double-destroy

    ; opts: { w, pad, flags, dark, font: {face, size} }
    __New(title, opts := {}) {
        _a2dlg_init()
        this._w := opts.HasProp("w") ? opts.w : 480
        this._pad := opts.HasProp("pad") ? opts.pad : 14
        flags := opts.HasProp("flags") ? opts.flags : "-MaximizeBox -MinimizeBox"
        this._y := this._pad
        this.dark := opts.HasProp("dark") ? opts.dark : a2dlg_is_dark()
        this.c := a2dlg_colors(this.dark)
        if opts.HasProp("font") {
            if opts.font.HasProp("face")
                this._face := opts.font.face
            if opts.font.HasProp("size")
                this._fsz := opts.font.size
        }

        this.gui := Gui(flags, title)
        this.gui.BackColor := this.c.bg
    }

    ; Computed read-only property
    hwnd => this.gui.Hwnd

    ; ----------------------------------------------------------------
    ;  Content builders  (most return `this` for optional chaining)
    ; ----------------------------------------------------------------

    ; Large title line with an optional 32×32 icon to the left.
    header(text, icon_path := "") {
        pad := this._pad
        y := this._y
        if (icon_path && FileExist(icon_path)) {
            try this.gui.AddPicture("x" pad " y" y " w32 h32", icon_path)
            this.gui.SetFont("s" (this._fsz + 2) " w700 c" this.c.text, this._face)
            this.gui.AddText("x" (pad + 40) " y" (y + 8) " w" (this._w - pad - 40 - pad), text)
        } else {
            this.gui.SetFont("s" (this._fsz + 2) " w700 c" this.c.text, this._face)
            this.gui.AddText("x" pad " y" (y + 4) " w" (this._w - pad * 2), text)
        }
        this._y += 48
        return this
    }

    ; Thin 2px horizontal separator followed by a small gap.
    sep() {
        this.gui.SetFont("s1")
        this.gui.AddText("x0 y" this._y " w" this._w " h2 Background" this.c.sep)
        this._y += 10
        return this
    }

    ; Colored icon glyph (s11) + main label (s10) + optional smaller subtext below.
    ; Returns {icon: ctrl, text: ctrl} so either can be updated later.
    row(icon, color, text, subtext := "") {
        pad := this._pad
        y := this._y
        this.gui.SetFont("s" (this._fsz + 1) " c" color, this._face)
        icon_ctrl := this.gui.AddText("x" pad " y" (y + 4) " w20 h18", icon)
        this.gui.SetFont("s" this._fsz " c" this.c.text, this._face)
        text_ctrl := this.gui.AddText("x" (pad + 24) " yp w" (this._w - pad * 2 - 24) " h18", text)
        this._y += 26
        if subtext {
            this.gui.SetFont("s" (this._fsz - 1) " c" this.c.sub, this._face)
            this.gui.AddText("x" (pad + 24) " y" this._y " w" (this._w - pad * 2 - 24), subtext)
            this._y += 20
        }
        return { icon: icon_ctrl, text: text_ctrl }
    }

    ; Like row() but starts muted (sub color) — intended for async checks.
    ; Update .icon.Text / .icon.SetFont() and .text.Text / .text.SetFont()
    ; when the check result is known.  Returns {icon: ctrl, text: ctrl}.
    row_pending(icon := "…", text := "") {
        pad := this._pad
        y := this._y
        this.gui.SetFont("s" (this._fsz + 1) " c" this.c.sub, this._face)
        icon_ctrl := this.gui.AddText("x" pad " y" (y + 4) " w20 h18", icon)
        this.gui.SetFont("s" this._fsz " c" this.c.sub, this._face)
        text_ctrl := this.gui.AddText("x" (pad + 24) " yp w" (this._w - pad * 2 - 24) " h18", text)
        this._y += 26
        return { icon: icon_ctrl, text: text_ctrl }
    }

    ; Small s9 caption in the sub color.  Returns the Text ctrl (update via .Value).
    text(content, ahk_opts := "") {
        pad := this._pad
        opts := ahk_opts ? " " ahk_opts : ""
        this.gui.SetFont("s" (this._fsz - 1) " c" this.c.sub, this._face)
        ctrl := this.gui.AddText("x" pad " y" this._y " w" (this._w - pad * 2) " h18" opts, content)
        this._y += 22
        return ctrl
    }

    ; Extra vertical whitespace.
    space(px := 8) {
        this._y += px
        return this
    }

    ; ----------------------------------------------------------------
    ;  Buttons
    ; ----------------------------------------------------------------

    ; Single flat button placed with a raw AHK option string.
    ; Use btn_row / btn_row_right for grouped layouts.
    btn(label, bg, fg, ahk_opts := "") {
        this.gui.SetFont("s" this._fsz " w600", this._face)
        ctrl := this.gui.AddButton(ahk_opts, label)
        a2dlg_make_button(ctrl, bg, fg)
        this._btn_hwnds.Push(ctrl.Hwnd)
        return ctrl
    }

    ; A horizontal row of flat buttons, left-aligned from the left margin.
    ;   specs : [{label, bg, fg [, opts]}, ...]
    ;   h     : button height (default 30)
    ;   gap   : spacing between buttons (default 8)
    ;   bw    : explicit per-button width; 0 = auto-distribute across full content width
    ; Advances _y by h + gap.  Returns array of controls in spec order.
    btn_row(specs, h := 30, gap := 8, bw := 0) {
        this.gui.SetFont("s" this._fsz " w600", this._face)
        pad := this._pad
        n := specs.Length
        if !bw
            bw := (this._w - pad * 2 - gap * (n - 1)) // n
        controls := []
        for i, s in specs {
            x_opt := (i = 1) ? "x" pad " y" this._y : "x+" gap " yp"
            extra := s.HasProp("opts") ? " " s.opts : ""
            ctrl := this.gui.AddButton(x_opt " w" bw " h" h extra, s.label)
            a2dlg_make_button(ctrl, s.bg, s.fg)
            this._btn_hwnds.Push(ctrl.Hwnd)
            controls.Push(ctrl)
        }
        this._y += h + gap
        return controls
    }

    ; A horizontal row of flat buttons, right-aligned (typical footer layout).
    ;   specs : [{label, bg, fg [, opts]}, ...]
    ;   bw    : uniform button width (default 100)
    ;   h     : button height (default 28)
    ;   gap   : spacing between buttons (default 8)
    ; Advances _y by h + pad.  Returns array of controls in spec order (left → right).
    btn_row_right(specs, bw := 100, h := 28, gap := 8) {
        this.gui.SetFont("s" this._fsz " w600", this._face)
        pad := this._pad
        n := specs.Length
        x0 := this._w - pad - bw * n - gap * (n - 1)
        controls := []
        for i, s in specs {
            x := x0 + (i - 1) * (bw + gap)
            extra := s.HasProp("opts") ? " " s.opts : ""
            ctrl := this.gui.AddButton("x" x " y" this._y " w" bw " h" h extra, s.label)
            a2dlg_make_button(ctrl, s.bg, s.fg)
            this._btn_hwnds.Push(ctrl.Hwnd)
            controls.Push(ctrl)
        }
        this._y += h + pad
        return controls
    }

    ; ----------------------------------------------------------------
    ;  Window management
    ; ----------------------------------------------------------------

    ; First show, centered on screen.
    ; extra_h reserves blank space below current content for a progressive reveal
    ; workflow: call show() early with headroom, add rows, call resize() each time.
    show(extra_h := 0) {
        this.gui.Show("w" this._w " h" (this._y + extra_h) " Center")
        a2dlg_apply_dark_title_bar(this.hwnd, this.dark)
        return this
    }

    ; Resize without moving or activating — use after adding content progressively.
    resize(extra_h := 0) {
        this.gui.Show("w" this._w " h" (this._y + extra_h) " NA")
        return this
    }

    ; Set the title-bar and taskbar icon from a file path.
    set_icon(path) {
        if !FileExist(path)
            return this
        hIcon := DllCall("LoadImage", "Ptr", 0, "Str", path,
            "UInt", 1, "Int", 0, "Int", 0, "UInt", 0x10, "Ptr")
        SendMessage(0x80, 0, hIcon, this.hwnd)   ; WM_SETICON ICON_SMALL
        SendMessage(0x80, 1, hIcon, this.hwnd)   ; WM_SETICON ICON_BIG
        return this
    }

    ; Bind Esc (while this window is active) to fn, or ExitApp() if omitted.
    esc_to_close(fn := "") {
        if !fn
            fn := (*) => ExitApp()
        HotIfWinActive("ahk_id " this.hwnd)
        Hotkey("Escape", fn)
        HotIfWinActive()
        return this
    }

    ; Register a handler for the Gui Close event (X button / Alt-F4).
    on_close(fn) {
        this.gui.OnEvent("Close", fn)
        return this
    }

    ; Register a handler for the Gui Escape event (Escape key while window is active).
    on_escape(fn) {
        this.gui.OnEvent("Escape", fn)
        return this
    }

    ; Destroy the window and remove all registered button HWNDs from _flat_buttons.
    ; Safe to call more than once (guarded by _destroyed).
    destroy() {
        if this._destroyed
            return
        this._destroyed := true
        global _flat_buttons, _flat_btn_hover
        for hwnd in this._btn_hwnds {
            _flat_buttons.Delete(hwnd)
            if (_flat_btn_hover = hwnd)
                _flat_btn_hover := 0
        }
        this._btn_hwnds := []
        this.gui.Destroy()
    }
}


; Register ctrl as owner-drawn with custom bg/fg ("RRGGBB" hex strings).
; Call after AddButton. Works before or after Gui.Show().
a2dlg_make_button(ctrl, bg, fg) {
    _a2dlg_init()
    global _flat_buttons
    hwnd := ctrl.Hwnd
    ; Register FIRST — WM_DRAWITEM can fire synchronously during the style change below
    _flat_buttons[hwnd] := { bg: bg, fg: fg, text: ctrl.Text }
    ; Switch style bits to BS_OWNERDRAW (0xB), keeping all other flags
    style := DllCall("GetWindowLongPtr", "Ptr", hwnd, "Int", -16, "Ptr")
    DllCall("SetWindowLongPtr", "Ptr", hwnd, "Int", -16, "Ptr", (style & ~0xF) | 0xB)
    ; Synchronous full repaint — button never flashes with the default look
    DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
    DllCall("UpdateWindow", "Ptr", hwnd)
}

; True when Windows "Apps use dark mode" is on.
a2dlg_is_dark() {
    try return !RegRead("HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        "AppsUseLightTheme")
    return false
}

; Standard a2 color scheme. Keys: bg, text, sub, sep, ok, warn, err, btn_bg, acc_fg.
a2dlg_colors(dark) {
    if (dark)
        return {
            bg: "202020",
            text: "E8E8E8",
            sub: "888888",
            sep: "444444",
            ok: "36EC95",
            warn: "FFA040",
            err: "FF5050",
            btn_bg: "2D2D2D",
            acc_fg: "1A1A1A"
        }
    return {
        bg: "F0F0F0",
        text: "1A1A1A",
        sub: "666666",
        sep: "C8C8C8",
        ok: "1A9E60",
        warn: "CC7000",
        err: "CC2020",
        btn_bg: "D8D8D8",
        acc_fg: "F8F8F8"
    }
}

; Apply a dark or light DWM title bar (Windows 10 1809+ / Windows 11).
a2dlg_apply_dark_title_bar(hwnd, dark) {
    val := dark ? 1 : 0
    try DllCall("dwmapi\DwmSetWindowAttribute",
        "Ptr", hwnd, "UInt", 20, "Int*", val, "UInt", 4)
}

/**
 * one-time library initializer — called lazily from a2dlg_make_button / A2Dialog.__New
 * No top-level executable code: the library is safe to #Include <a2dlg> without warnings.
 */
_a2dlg_init() {
    static _done := false
    if _done
        return
    _done := true
    global _flat_buttons, _flat_btn_hover
    _flat_buttons   := Map()
    _flat_btn_hover := 0
    OnMessage(0x2B,  _flat_btn_on_draw)        ; WM_DRAWITEM
    OnMessage(0x200, _flat_btn_on_mouse_move)  ; WM_MOUSEMOVE
    OnMessage(0x2A3, _flat_btn_on_mouse_leave) ; WM_MOUSELEAVE
}

; ================================================================
;  Internal — WM_DRAWITEM handler and GDI helpers
; ================================================================

; WM_DRAWITEM handler — called by Windows whenever a registered button needs painting.
; DRAWITEMSTRUCT offsets (x64):
;   0  CtlType (UInt)   4  CtlID   8  itemID   12 itemAction
;  16  itemState (UInt) 20 (pad)  24  hwndItem (Ptr)   32  hDC (Ptr)
;  40  rcItem.left  44  .top  48  .right  52  .bottom  (all Int)
_flat_btn_on_draw(wParam, lParam, *) {
    global _flat_buttons
    if (NumGet(lParam, 0, "UInt") != 4)     ; CtlType must be ODT_BUTTON = 4
        return
    hwnd := NumGet(lParam, 24, "Ptr")
    if !_flat_buttons.Has(hwnd)
        return

    s := _flat_buttons[hwnd]
    state := NumGet(lParam, 16, "UInt")
    hDC := NumGet(lParam, 32, "Ptr")

    ; Full button bounding rect from DRAWITEMSTRUCT.rcItem
    rc := Buffer(16)
    NumPut("Int", NumGet(lParam, 40, "Int"), rc, 0)    ; left
    NumPut("Int", NumGet(lParam, 44, "Int"), rc, 4)    ; top
    NumPut("Int", NumGet(lParam, 48, "Int"), rc, 8)    ; right
    NumPut("Int", NumGet(lParam, 52, "Int"), rc, 12)    ; bottom

    ; Fill background: darken when pressed, lighten when hovered, plain otherwise
    bg := (state & 0x1) ? _flat_btn_dim(s.bg)
        : (_flat_btn_hover = hwnd) ? _flat_btn_lit(s.bg)
            : s.bg
    hBrush := DllCall("CreateSolidBrush", "UInt", _flat_btn_gdi(bg), "Ptr")
    DllCall("FillRect", "Ptr", hDC, "Ptr", rc, "Ptr", hBrush)
    DllCall("DeleteObject", "Ptr", hBrush)

    ; Draw label using the font AHK set on the button control
    hFont := SendMessage(0x31, 0, 0, hwnd)   ; WM_GETFONT
    old_font := DllCall("SelectObject", "Ptr", hDC, "Ptr", hFont, "Ptr")
    DllCall("SetBkMode", "Ptr", hDC, "Int", 1)                  ; TRANSPARENT
    DllCall("SetTextColor", "Ptr", hDC, "UInt", _flat_btn_gdi(s.fg))
    DllCall("DrawTextW", "Ptr", hDC, "WStr", s.text, "Int", -1,
        "Ptr", rc, "UInt", 0x25)                                    ; DT_CENTER|DT_VCENTER|DT_SINGLELINE
    DllCall("SelectObject", "Ptr", hDC, "Ptr", old_font)

    ; Dotted focus ring when the button has keyboard focus (ODS_FOCUS = 0x10)
    if (state & 0x10) {
        inner := Buffer(16)
        NumPut("Int", NumGet(rc, 0, "Int") + 3, inner, 0)
        NumPut("Int", NumGet(rc, 4, "Int") + 3, inner, 4)
        NumPut("Int", NumGet(rc, 8, "Int") - 3, inner, 8)
        NumPut("Int", NumGet(rc, 12, "Int") - 3, inner, 12)
        DllCall("DrawFocusRect", "Ptr", hDC, "Ptr", inner)
    }
    return true
}

; "RRGGBB" hex string → Win32 COLORREF (0x00BBGGRR little-endian)
_flat_btn_gdi(hex) {
    r := Integer("0x" SubStr(hex, 1, 2))
    g := Integer("0x" SubStr(hex, 3, 2))
    b := Integer("0x" SubStr(hex, 5, 2))
    return r | (g << 8) | (b << 16)
}

; Darken each RGB channel by 30 (clamped) — pressed-state visual feedback
_flat_btn_dim(hex) {
    r := Max(0, Integer("0x" SubStr(hex, 1, 2)) - 30)
    g := Max(0, Integer("0x" SubStr(hex, 3, 2)) - 30)
    b := Max(0, Integer("0x" SubStr(hex, 5, 2)) - 30)
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

; Lighten each RGB channel by 15 (clamped) — hover-state visual feedback
_flat_btn_lit(hex) {
    r := Min(255, Integer("0x" SubStr(hex, 1, 2)) + 15)
    g := Min(255, Integer("0x" SubStr(hex, 3, 2)) + 15)
    b := Min(255, Integer("0x" SubStr(hex, 5, 2)) + 15)
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

; WM_MOUSEMOVE — fires on the button control; start tracking if not already.
; TRACKMOUSEEVENT (x64): cbSize DWORD@0, dwFlags DWORD@4, hwndTrack Ptr@8, dwHoverTime DWORD@16
_flat_btn_on_mouse_move(wParam, lParam, msg, hwnd) {
    global _flat_buttons, _flat_btn_hover
    if !_flat_buttons.Has(hwnd) || (_flat_btn_hover = hwnd)
        return
    _flat_btn_hover := hwnd
    tme := Buffer(24, 0)
    NumPut("UInt", 24, tme, 0)   ; cbSize
    NumPut("UInt", 0x2, tme, 4)   ; dwFlags = TME_LEAVE
    NumPut("Ptr", hwnd, tme, 8)   ; hwndTrack
    DllCall("TrackMouseEvent", "Ptr", tme)
    DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
    DllCall("UpdateWindow", "Ptr", hwnd)
}

; WM_MOUSELEAVE — fires on the button that called TrackMouseEvent when the cursor leaves.
_flat_btn_on_mouse_leave(wParam, lParam, msg, hwnd) {
    global _flat_buttons, _flat_btn_hover
    if (_flat_btn_hover != hwnd)
        return
    _flat_btn_hover := 0
    if _flat_buttons.Has(hwnd) {
        DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
        DllCall("UpdateWindow", "Ptr", hwnd)
    }
}

; ================================================================
;  Popup dialog functions
;
;   a2dlg_info(msg [, title])                    — info message + OK
;   a2dlg_error(msg [, title, error_detail])     — error + selectable detail + OK
;   a2dlg_yes_no(msg [, title])                  → true / false
;   a2dlg_ok_cancel(msg [, title])               → true / false
;   a2dlg_input(msg [, title, default_text])     → "" (cancelled) or user string
;
;  All functions block until the user dismisses the dialog.
; ================================================================

; Shared helper: add icon + message body to dialog, return body content height.
_a2dlg_icon_msg(d, icon_glyph, icon_color, msg) {
    c := d.c
    inner_w := d._w - d._pad * 2
    ; Icon — large, colored
    d.gui.SetFont("s18 w700 c" icon_color, d._face)
    d.gui.AddText("x" d._pad " y" d._y " w30 h30 Center", icon_glyph)
    ; Message — wrap within remaining width
    d.gui.SetFont("s" d._fsz " w400 c" c.text, d._face)
    msg_x := d._pad + 36
    msg_w := inner_w - 36
    msg_ctrl := d.gui.AddText("x" msg_x " y" d._y " w" msg_w " Wrap", msg)
    msg_ctrl.GetPos(, , , &mh)
    d._y += Max(34, mh + 4)
    return msg_ctrl
}

; ----------------------------------------------------------------
;  a2dlg_info — informational popup, OK button
; ----------------------------------------------------------------
a2dlg_info(msg, title := "a2 Information", dark := unset) {
    opts := { w: 380, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if IsSet(dark)
        opts.dark := dark
    d := A2Dialog(title, opts)
    c := d.c
    d.space(4)
    _a2dlg_icon_msg(d, "ℹ️", c.ok, msg)
    d.space(6)
    d.sep()
    buttons := d.btn_row_right([{ label: "OK", bg: c.ok, fg: c.acc_fg, opts: "Default" }])
    buttons[1].OnEvent("Click", (*) => d.destroy())
    d.on_close((*) => d.destroy())
    d.on_escape((*) => d.destroy())
    d.show()
    WinWaitClose("ahk_id " d.hwnd)
}

; ----------------------------------------------------------------
;  a2dlg_error — error popup with optional selectable detail text, OK button
; ----------------------------------------------------------------
a2dlg_error(msg, title := "a2 Error", error_detail := "", dark := unset) {
    opts := { w: 420, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if IsSet(dark)
        opts.dark := dark
    d := A2Dialog(title, opts)
    c := d.c
    d.space(4)
    _a2dlg_icon_msg(d, "❌", c.err, msg)
    if (error_detail != "") {
        d.space(4)
        detail_bg := d.dark ? "181818" : "FFFFFF"
        detail_fg := d.dark ? "CC6666" : "990000"
        d.gui.SetFont("s" (d._fsz - 1) " w400 c" detail_fg, "Consolas")
        inner_w := d._w - d._pad * 2
        edit := d.gui.AddEdit(
            "x" d._pad " y" d._y " w" inner_w " h64 ReadOnly -E0x200 Background" detail_bg,
            error_detail)
        d._y += 72
    }
    d.space(6)
    d.sep()
    buttons := d.btn_row_right([{ label: "OK", bg: c.err, fg: "F8F8F8", opts: "Default" }])
    buttons[1].OnEvent("Click", (*) => d.destroy())
    d.on_close((*) => d.destroy())
    d.on_escape((*) => d.destroy())
    d.show()
    WinWaitClose("ahk_id " d.hwnd)
}

; ----------------------------------------------------------------
;  a2dlg_yes_no — question dialog → true (Yes) / false (No)
; ----------------------------------------------------------------
a2dlg_yes_no(msg, title := "a2", dark := unset) {
    opts := { w: 360, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if IsSet(dark)
        opts.dark := dark
    d := A2Dialog(title, opts)
    c := d.c
    d.space(4)
    _a2dlg_icon_msg(d, "❓", c.warn, msg)
    d.space(6)
    d.sep()
    buttons := d.btn_row_right([{ label: "Yes", bg: c.ok, fg: c.acc_fg, opts: "Default" }, { label: "No", bg: c.btn_bg,
        fg: c.text }])
    result := false
    buttons[1].OnEvent("Click", (*) => (result := true, d.destroy()))
    buttons[2].OnEvent("Click", (*) => d.destroy())
    d.on_close((*) => d.destroy())
    d.on_escape((*) => d.destroy())
    d.show()
    WinWaitClose("ahk_id " d.hwnd)
    return result
}

; ----------------------------------------------------------------
;  a2dlg_ok_cancel — confirmation dialog → true (OK) / false (Cancel)
; ----------------------------------------------------------------
a2dlg_ok_cancel(msg, title := "a2", dark := unset) {
    opts := { w: 360, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if IsSet(dark)
        opts.dark := dark
    d := A2Dialog(title, opts)
    c := d.c
    d.space(4)
    _a2dlg_icon_msg(d, "❓", c.warn, msg)
    d.space(6)
    d.sep()
    buttons := d.btn_row_right([{ label: "OK", bg: c.ok, fg: c.acc_fg, opts: "Default" }, { label: "Cancel", bg: c.btn_bg,
        fg: c.text }])
    result := false
    buttons[1].OnEvent("Click", (*) => (result := true, d.destroy()))
    buttons[2].OnEvent("Click", (*) => d.destroy())
    d.on_close((*) => d.destroy())
    d.on_escape((*) => d.destroy())
    d.show()
    WinWaitClose("ahk_id " d.hwnd)
    return result
}

; ----------------------------------------------------------------
;  a2dlg_input — text input dialog → "" (cancelled) or entered string
; ----------------------------------------------------------------
a2dlg_input(msg, title := "a2 Input", default_text := "", dark := unset) {
    opts := { w: 380, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if IsSet(dark)
        opts.dark := dark
    d := A2Dialog(title, opts)
    c := d.c
    d.space(4)
    _a2dlg_icon_msg(d, "✏️", c.ok, msg)
    d.space(4)
    inner_w := d._w - d._pad * 2
    edit_bg := d.dark ? "2A2A2A" : "FFFFFF"
    d.gui.SetFont("s" d._fsz " w400 c" c.text, d._face)
    edit := d.gui.AddEdit(
        "x" d._pad " y" d._y " w" inner_w " h24 Background" edit_bg,
        default_text)
    d._y += 32
    d.space(6)
    d.sep()
    buttons := d.btn_row_right([{ label: "OK", bg: c.ok, fg: c.acc_fg, opts: "Default" }, { label: "Cancel", bg: c.btn_bg,
        fg: c.text }])
    value := default_text       ; preset; updated on OK, stays default_text on Cancel/close
    cancelled := false
    buttons[1].OnEvent("Click", (*) => (value := edit.Value, d.destroy()))
    buttons[2].OnEvent("Click", (*) => (cancelled := true, d.destroy()))
    d.on_close((*) => (cancelled := true, d.destroy()))
    d.on_escape((*) => (cancelled := true, d.destroy()))
    d.show()
    edit.Focus()
    WinWaitClose("ahk_id " d.hwnd)
    return cancelled ? "" : value
}
