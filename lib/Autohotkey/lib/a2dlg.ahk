/************************************************************************
 * a2dlg.ahk - reusable dialog helpers for a2
 *
 * Low-level (function-based):
 *  a2dlg_make_button(ctrl, bg, fg)              - owner-drawn button with custom colors
 *  a2dlg_colors(dark)                    - standard a2 color scheme object
 *  a2dlg_apply_dark_title_bar(hwnd, dark) - DWM dark/light title bar
 * High-level (A2Dialog class):
 *   d := A2Dialog(title [, opts])            - opts: w, pad, flags, dark, font: {face, size}
 *   d.header(text [, icon_path])             - large title with optional 32px icon
 *   d.sep()                                  - thin horizontal separator line
 *   d.row(icon, color, text [, subtext])     - colored icon + label row => {icon, text}
 *   d.row_pending([icon, text])              - muted row for live update => {icon, text}
 *   d.text(content [, ahk_opts])             - small caption / status line => ctrl
 *   d.space(px)                              - extra vertical gap
 *   d.btn(label, [bg, fg , ahk_opts])        - single flat button => ctrl
 *   d.btn_row(specs [, h, gap, bw])          - left-aligned button row => [controls]
 *   d.btn_row_right(specs [, bw, h, gap])    - right-aligned footer row => [controls]
 *  Per-button width override: add w to a spec, e.g. {label: "X", bg:…, fg:…, w: 120}
 *   d.show([extra_h], [center_on_window])    - first show, centered on screen or on
 *                                              window of given handle.
 *   d.resize([extra_h])                      - resize in-place (progressive reveal)
 *   d.set_icon(path)                         - set window title-bar / taskbar icon
 *   d.esc_to_close([fn])                     - Esc closes or calls fn
 *   d.on_close(fn)                           - register Gui Close handler
 *   d.destroy()                              - destroy window and clean up btn registry
 *   d.gui  d.hwnd  d.c  d.dark              - direct access to underlying objects
 *  Button specs (for btn_row / btn_row_right): array of {label, bg, fg [, opts]}
 *    opts: extra AHK button option string, e.g. "Default"
 *  Color strings are always 6-digit "RRGGBB" hex (no #).
 *  Include this file once per script - it self-registers the WM_DRAWITEM handler.
 ***********************************************************************/
#Include <string>
#Include <a2tip>
#Include <window>
#Include <windows>

/**
 * A2Dialog - composable dialog builder
 */
class A2Dialog {
    ; Font face used in the dialog.
    font_face := "Segoe UI"
    ; Base font size - all other sizes derived from this
    font_size := 10

    _icon := ""
    a2_icon := A_LineFile "\..\..\..\..\ui\res\a2.ico"

    _pos := ""
    _btn_hwnds := [] ; tracked for cleanup in destroy()
    _destroyed := false ; guard against double-destroy
    _exit_on_close := false

    ; Result variable for OK/Cancel dialog.
    cancelled := true
    ; Result variable for arbitrary dialogs.
    result := ""
    ; Message variable for arbitrary dialogs.
    msg := ""

    /**
     * Create a new A2Dialog.
     * @example
     *      dlg := A2Dialog("My Dialog", {w: 400, dark: true})
     *
     * @param {String} title
     * Window title
     * @param {(Object)} opts
     * Options: {w, pad, flags, dark, font: {face, size}}
     */
    __New(title, opts := {}) {
        _a2dlg_init()
        ; Total width of the dialog.
        this.width := opts.HasProp("w") ? opts.w : 480
        ; Total height of the dialog.
        this.height := this.pad
        ; Padding value for spacing.
        this.pad := opts.HasProp("pad") ? opts.pad : 14
        this.dark := opts.HasProp("dark") ? opts.dark : windows_is_dark()
        ; Color Object with keys: bg, text, sub, sep, ok, warn, err, btn_bg, acc_fg
        this.c := a2dlg_colors(this.dark)
        if opts.HasProp("font") {
            if opts.font.HasProp("face")
                this.font_face := opts.font.face
        if opts.font.HasProp("size")
            this.font_size := opts.font.size
    }

        if opts.HasProp("x") && opts.HasProp("y")
            this._pos := "x" opts.x " y" opts.y

        flags := opts.HasProp("flags") ? opts.flags : "-MaximizeBox -MinimizeBox"
        this.gui := Gui(flags, title)
        this.gui.BackColor := this.c.bg

        if opts.HasProp("icon") && FileExist(opts.icon) {
            this.set_icon(opts.icon)
        } else {
            this.set_icon(this.a2_icon)
        }
    }

    /** Read-only HWND of the underlying Gui. */
    hwnd => this.gui.Hwnd

    ; Content builders:  (most return `this` for optional chaining)

    /**
     * Large title line with an optional 32×32 icon to the left.
     *
     * @param {String} text
     * Title text to display
     * @param {String} icon_path
     * Optional icon file path; supports "file,N" registry format
     * @returns  this (chainable)
     */
    header(text, icon_path := "") {
        pad := this.pad
        y := this.height
        icon_file := icon_path
        icon_opt := ""
        if InStr(icon_path, ",") {
            parts := StrSplit(icon_path, ",", , 2)
            icon_file := parts[1]
            try n := Integer(parts[2])
            if IsSet(n)
                icon_opt := "Icon" (n >= 0 ? n + 1 : n)
        }
        this.gui.SetFont("s" (this.font_size + 2) " w700 c" this.c.text, this.font_face)
        if (icon_file && FileExist(icon_file)) {
            try this.gui.AddPicture("x" pad " y" y " w32 h32 " icon_opt, icon_file)
            this.gui.AddText("x" (pad + 40) " y" (y + 8) " w" (this.width - pad - 40 - pad), text)
        } else {
            this.gui.AddText("x" pad " y" (y + 4) " w" (this.width - pad * 2), text)
        }
        this.space(48)
        return this
    }

    /**
     * Add a thin 2px horizontal separator line followed by a small gap.
     * @returns  this (chainable)
     */
    sep() {
        this.gui.SetFont("s1")
        this.gui.AddText("x0 y" this.height " w" this.width " h2 Background" this.c.sep)
        this.space(10)
        return this
    }

    /**
     * Colored icon glyph + main label + optional smaller subtext below.
     *
     * @param {String} glyph - Glyph or emoji for the first column.
     * @param {String} text - Main label text.
     * @param {String} [color] - Optional 6-digit RRGGBB hex color for the icon
     * @param {String} [subtext] - Optional muted line below the label
     * @param {Boolean} [active] - Optional muted line below the label
     * @returns  {icon: ctrl, text: ctrl} - either can be updated later
     */
    glyph_row(glyph, text, color := "", subtext := "", active := true) {
        if !color
            color := this.c.text
        pad := this.pad
        y := this.height
        this.gui.SetFont("s" (this.font_size + 1) " w400 c" color, this.font_face)
        glyph_ctrl := this.gui.AddText("x" pad " y" (y + 4) " w20 h18", glyph)
        ; Store color so we can toggle without needing the color scheme
        glyph_ctrl.color_on := color
        if !active
            glyph_ctrl.SetFont("c" this.c.sub)
        this.gui.SetFont("s" this.font_size " w400 c" color, this.font_face)
        text_ctrl := this.gui.AddText("x" (pad + 24) " yp w" (this.width - pad * 2 - 24) " h18", text)
        text_ctrl.color_on := color
        this.space(26)
        if subtext {
            this.gui.SetFont("s" (this.font_size - 1) " c" this.c.sub, this.font_face)
            this.gui.AddText("x" (pad + 24) " y" this.height " w" (this.width - pad * 2 - 24), subtext)
            this.space(20)
        }
        return { glyph: glyph_ctrl, text: text_ctrl, items: [glyph_ctrl, text_ctrl] }
    }

    /**
     * Restore each control to its original color_on color.
     * Accepts individual controls or glyph_row return values (which have an .items array).
     *
     * @param {Any*} items  Controls or row refs to activate (variadic)
     * @returns  this (chainable)
     */
    set_active(items*) {
        for item in items {
            if item.HasProp('items') {
                for sub_item in item.items
                    sub_item.SetFont("c" sub_item.color_on)
            } else {
                item.SetFont("c" item.color_on)
            }
        }
        return this
    }

    /**
     * Set each control to the muted subtitle color (c.sub).
     * Accepts individual controls or glyph_row return values (which have an .items array).
     *
     * @param {Any*} items  Controls or row refs to deactivate (variadic)
     * @returns  this (chainable)
     */
    set_inactive(items*) {
        this.set_color(this.c.sub, items*)
        return this
    }

    /**
     * Set each control to an arbitrary color.
     * Accepts individual controls or glyph_row return values (which have an .items array).
     *
     * @param {String} color  6-digit RRGGBB hex color to apply
     * @param {Any*} items    Controls or row refs to recolor (variadic)
     * @returns  this (chainable)
     */
    set_color(color, items*) {
        for item in items {
            if item.HasProp('items') {
                for sub_item in item.items
                    sub_item.SetFont("c" color)
            } else {
                item.SetFont("c" color)
            }
        }
        return this
    }

    /**
     * Like row() but starts muted - intended for async status rows.
     * Update .icon and .text controls once the result is known.
     *
     * @param {String} icon
     * Initial glyph, default "…"
     * @param {String} text
     * Initial label text
     * @returns  {icon: ctrl, text: ctrl}
     */
    row_pending(icon := "…", text := "") {
        pad := this.pad
        y := this.height
        this.gui.SetFont("s" (this.font_size + 1) " c" this.c.sub, this.font_face)
        glyph_ctrl := this.gui.AddText("x" pad " y" (y + 4) " w20 h18", icon)
        this.gui.SetFont("s" this.font_size " c" this.c.sub, this.font_face)
        text_ctrl := this.gui.AddText("x" (pad + 24) " yp w" (this.width - pad * 2 - 24) " h18", text)
        this.space(26)
        return { icon: glyph_ctrl, text: text_ctrl }
    }

    /**
     * Bold sub-section heading (font_size+1, text color).
     *
     * @param {String} text
     * Heading text
     * @returns  Text ctrl
     */
    heading(text) {
        pad := this.pad
        this.gui.SetFont("s" (this.font_size + 1) " w700 c" this.c.text, this.font_face)
        ctrl := this.gui.AddText("x" pad " y" this.height " w" (this.width - pad * 2), text)
        this.space(24)
        return ctrl
    }

    /**
     * Small muted caption. Wraps and auto-sizes to the rendered height.
     *
     * @param {String} content
     * Text to display
     * @param {String} ahk_opts
     * Extra AHK control option string appended to the AddText call
     * @returns  Text ctrl
     */
    text(content, color := "", ahk_opts := "") {
        if !color
            color := this.c.sub
        pad := this.pad
        opts := ahk_opts ? " " ahk_opts : ""
        this.gui.SetFont("s" (this.font_size - 1) " c" color, this.font_face)
        ctrl := this.gui.AddText("x" pad " y" this.height " w" (this.width - pad * 2) " Wrap" opts, content)
        ctrl.GetPos(, , , &h)
        this.space(h + 6)
        return ctrl
    }

    /**
     * 22×22 picture on the left + wrapped sub-text on the right.
     *
     * @param {String} file
     * Path to the image or executable file
     * @param {String} opt
     * Extra AHK picture option string (e.g. "Icon3"), or ""
     * @param {String} text
     * Caption text displayed to the right of the picture
     * @returns  {pic: ctrl, text: ctrl} - pic is "" if the file is missing
     */
    pic_row(file, opt, text) {
        pad := this.pad
        y := this.height
        pic_ctrl := ""
        if (file && FileExist(file))
            try pic_ctrl := this.gui.AddPicture("x" pad " y" y " w22 h22 " opt, file)
        this.gui.SetFont("s" (this.font_size - 1) " c" this.c.sub, this.font_face)
        txt_ctrl := this.gui.AddText("x" (pad + 28) " y" (y + 4)
        " w" (this.width - pad * 2 - 28) " Wrap", text)
        txt_ctrl.GetPos(, , , &h)
        this.space(Max(28, h + 8))
        return { pic: pic_ctrl, text: txt_ctrl }
    }

    /**
     * Lay out array of pictures in a horizontal strip, auto-clipped to content width.
     *
     * @param {Array} items
     * Each item is a file path string, or {file [, opt]} for extra AHK picture options
     * @param {Integer} size
     * Width and height of each picture in pixels (default 32)
     * @param {Integer} gap
     * Spacing between pictures in pixels (default 8)
     * @returns {Integer} Count of pictures actually shown.
     */
    pic_strip(items, size := 32, gap := 8) {
        pad := this.pad
        slot := size + gap
        n := Min(items.Length, (this.width - pad * 2 + gap) // slot)
        loop n {
            item := items[A_Index]
            file_path := (item is String) ? item : item.file
            opt := (item is String || !item.HasProp("opt")) ? "" : item.opt
            try this.gui.AddPicture("x" (pad + (A_Index - 1) * slot) " y" this.height
            " w" size " h" size " " opt, file_path)
        }
        this.space(size + 4)
        return n
    }

    /**
     * Add extra vertical whitespace.
     *
     * @param {Integer} px
     * Pixels to advance (default 8)
     * @returns  this (chainable)
     */
    space(px := 8) {
        this.height += px
        return this
    }

    ; Buttons

    /**
     * Single flat button placed with a raw AHK option string.
     * Use btn_row / btn_row_right for grouped layouts.
     *
     * @param {String} label
     * Button label text.
     * @param {String} [ahk_opts]
     * Optional AHK button option string (e.g. "x10 y20 w80 h28").
     * @param {String} [bg]
     * Optional Background color, 6-digit RRGGBB hex.
     * @param {String} [fg]
     * Optional Foreground (text) color, 6-digit RRGGBB hex.
     * @returns Button ctrl
     */
    btn(label, ahk_opts := "", bg := "", fg := "") {
        bg := bg ? bg : this.c.btn_bg
        fg := fg ? fg : this.c.text
        this.gui.SetFont("s" this.font_size " w600", this.font_face)
        ctrl := this.gui.AddButton(ahk_opts, label)
        a2dlg_make_button(ctrl, bg, fg)
        this._btn_hwnds.Push(ctrl.Hwnd)
        return ctrl
    }

    /**
     * Horizontal row of flat buttons, left-aligned from the left margin.
     *
     * @param {Array} specs
     * Array of {`label`, [`bg`, `fg` , `opts`]} - optional for colors: `bg`, `fg`.
     * `opts` for extra AHK button option string.
     * @param {Integer} h
     * Button height in pixels (default 30)
     * @param {Integer} gap
     * Spacing between buttons in pixels (default 8)
     * @param {Integer} bw
     * Per-button width; 0 = auto-distribute across full content width
     * @returns  Array of button controls in spec order
     */
    btn_row(specs, h := 30, gap := 8, bw := 0) {
        this.gui.SetFont("s" this.font_size " w600", this.font_face)
        pad := this.pad
        n := specs.Length
        if !bw
            bw := (this.width - pad * 2 - gap * (n - 1)) // n
        controls := []
        for i, s in specs {
            x_opt := (i = 1) ? "x" pad " y" this.height : "x+" gap " yp"
            extra := s.HasProp("opts") ? " " s.opts : ""
            ctrl := this.gui.AddButton(x_opt " w" bw " h" h extra, s.label)
            bg := s.HasProp("bg") ? s.bg : this.c.btn_bg
            fg := s.HasProp("fg") ? s.fg : this.c.text
            a2dlg_make_button(ctrl, bg, fg)
            this._btn_hwnds.Push(ctrl.Hwnd)
            controls.Push(ctrl)
        }
        this.space(h + gap)
        return controls
    }

    /**
     * Horizontal row of flat buttons, right-aligned - typical footer layout.
     *
     * Button width priority (highest → lowest):
     *   1. Per-spec w property  - {label: "X", bg:…, fg:…, w: 120}
     *   2. bw parameter         - uniform width for every button without a spec.w
     *   3. Auto (bw = 0)        - each button sizes to its label text
     *
     * @param {Array} specs
     * Array of {label, bg, fg [, opts, w]} - opts: extra AHK option string; w: per-button width
     * @param {Integer} bw
     * Uniform button width in pixels; 0 = auto-size each to its label (default 0)
     * @param {Integer} h
     * Button height in pixels (default 28)
     * @param {Integer} gap
     * Spacing between buttons in pixels (default 8)
     * @returns  Array of button controls in left => right order
     */
    btn_row_right(specs, bw := 0, h := 28, gap := 8) {
        this.gui.SetFont("s" this.font_size " w600", this.font_face)
        pad := this.pad
        controls := []
        widths := []

        ; Pass 1 - add every button at a throwaway position to resolve its final width.
        ; spec.w beats bw; bw=0 means auto-detect from the rendered control size.
        for spec in specs {
            extra := spec.HasProp("opts") ? " " spec.opts : ""
            w := spec.HasProp("w") ? spec.w : bw
            bg := spec.HasProp("bg") ? spec.bg : this.c.btn_bg
            fg := spec.HasProp("fg") ? spec.fg : this.c.text
            if w {
                ctrl := this.gui.AddButton("x0 y0 w" w " h" h extra, spec.label)
            } else {
                ctrl := this.gui.AddButton("x0 y0 h" h extra, spec.label)
                ctrl.GetPos(, , &w,)
            }
            a2dlg_make_button(ctrl, bg, fg)
            this._btn_hwnds.Push(ctrl.Hwnd)
            controls.Push(ctrl)
            widths.Push(w)
        }

        ; Pass 2 - right-align: compute start x from total width, then move each button.
        total_w := gap * (controls.Length - 1)
        for w in widths
            total_w += w
        x := this.width - pad - total_w
        for i, ctrl in controls {
            ctrl.Move(x, this.height, widths[i], h)
            x += widths[i] + gap
        }

        this.space(h + pad)
        return controls
    }

    /**
     * Add a right-aligned "Close" button that calls destroy().
     * Sets cancelled := false - closing is not cancelling.
     * @returns  this (chainable)
     */
    btn_close() {
        this.btn_row_right([{ label: "Close", bg: this.c.btn_bg, fg: this.c.text, opts: "Default" }])[1]
        .OnEvent("Click", (*) => this.destroy())
    }

    /**
     * Add a right-aligned OK + Cancel button pair.
     * OK sets cancelled := false and calls destroy(); Cancel just calls destroy().
     *
     * @param {Integer} [bw=80]           Uniform button width in pixels
     * @param {Func}    [on_ok]           Optional callback fired before destroy on OK
     * @param {String}  [ok_label="OK"]   Label override for the OK button
     * @param {String}  [cancel_label="Cancel"]  Label override for the Cancel button
     * @param {Boolean} [default_btn=true]  Whether OK gets the Default (Enter key) style
     * @returns  [ok_ctrl, cancel_ctrl]
     */
    btn_ok_cancel(bw := 80, on_ok := "", ok_label := "", cancel_label := "", default_btn := true) {
        ok_label := ok_label ? ok_label : "OK"
        cancel_label := cancel_label ? cancel_label : "Cancel"
        extra := default_btn ? "Default" : ""
        buttons := this.btn_row_right([
            { label: ok_label, bg: this.c.ok, fg: this.c.acc_fg, opts: extra},
            { label: cancel_label }],
            bw
        )
        buttons[1].OnEvent("Click", (*) => (
            on_ok ? on_ok() : 0,
            this.cancelled := false,
            this.destroy()
        ))
        buttons[2].OnEvent("Click", (*) => this.destroy())
        return buttons
    }

    /**
     * Add a right-aligned accent OK button that sets cancelled := false and calls destroy().
     *
     * @param {Integer} [bw=80]             Button width in pixels
     * @param {Func}    [on_ok]             Optional callback fired before destroy
     * @param {String}  [ok_label="OK"]     Label override
     * @param {String}  [bg]                Background color override (default c.ok)
     * @param {String}  [fg]                Foreground color override (default c.acc_fg)
     * @param {Boolean} [default_btn=true]  Whether the button gets the Default (Enter key) style
     * @returns  this (chainable)
     */
    btn_ok(bw := 80, on_ok := "", ok_label := "", bg := "", fg := "", default_btn := true) {
        ok_label := ok_label ? ok_label : "OK"
        bg := bg ? bg : this.c.ok
        fg := fg ? fg : this.c.acc_fg
        extra := default_btn ? "Default" : ""
        this.btn_row_right([{ label: ok_label, bg: bg, fg: fg, opts: extra}], bw)[1]
        .OnEvent("Click", (*) => (
            on_ok ? on_ok() : 0,
            this.cancelled := false,
            this.destroy()))
        return this
    }

    /**
     * Read-only monospaced text box - for error details, stack traces, generated code etc.
     *
     * @param {String}  text      Initial content
     * @param {Integer} [h=64]    Box height in pixels
     * @returns  Edit ctrl (Value can be updated later)
     */
    code_box(text, h := 64) {
        detail_bg := this.dark ? "181818" : "FFFFFF"
        this.gui.SetFont("s" (this.font_size - 1) " w400 c" this.c.sub, "Consolas")
        inner_w := this.width - this.pad * 2
        ctrl := this.gui.AddEdit(
            "x" this.pad " y" this.height " w" inner_w " h" h " ReadOnly -E0x200 Background" detail_bg,
            text)
        this.space(h + 8)
        return ctrl
    }

    /**
     * Single-line text input with a subtle underline separator below.
     *
     * @param {String} [default_text]  Pre-filled value
     * @returns  Edit ctrl
     */
    edit_field(default_text := "") {
        edit_bg := this.dark ? "181818" : "E8E8E8"
        inner_w := this.width - this.pad * 2
        this.gui.SetFont("s" this.font_size " w400 c" this.c.text, this.font_face)
        ctrl := this.gui.AddEdit(
            "x" this.pad " y" this.height " w" inner_w " h24 -Border -E0x200 Background" edit_bg,
            default_text)
        this.gui.AddText("x" this.pad " y" (this.height + 24) " w" inner_w " h1 Background" this.c.sep)
        this.space(32)
        return ctrl
    }

    ; Window management methods

    /**
     * First show, centered on screen.
     * Pass extra_h to reserve blank space for a progressive reveal workflow:
     * call show() early with headroom, add rows, call resize() each time.
     *
     * @param {Integer} [extra_h]
     * Extra pixels of height to reserve below current content (default 0)
     * @param {Integer} [center_on_window]
     * Optional window handle to center the dialog on. (Default 0 > centers on screen)
     * @returns  this (chainable)
     */
    show(extra_h := 0, center_on_window := 0) {
        w := this.width, h := this.height + extra_h
        options := "w" w " h" h " "
        if center_on_window {
            other_geo := window_get_geometry(center_on_window)
            this_geo := window_get_empty_geo()
            this_geo.w := w, this_geo.h := h
            window_center_geo(&this_geo, other_geo)
            options .= "x" this_geo.x " y" this_geo.y
        }
        else
            options .= this._pos ? this._pos : "Center"
        this.gui.Show(options)
        a2dlg_apply_dark_title_bar(this.hwnd, this.dark)
        return this
    }

    /**
     * Resize without moving or activating - use after adding content progressively.
     *
     * @param {Integer} extra_h
     * Extra pixels of height to reserve (default 0)
     * @returns  this (chainable)
     */
    resize(extra_h := 0) {
        this.gui.Show("w" this.width " h" (this.height + extra_h) " NA")
        return this
    }

    /**
     * Set the title-bar and taskbar icon.
     *
     * @param {String|Integer} path
     * File path to an ICO/EXE/DLL, or an HICON handle returned by icon_extract()
     * @returns  this (chainable)
     */
    set_icon(path) {
        if (path == this._icon)
            return
        this._icon := path

        if FileExist(path)
            hIcon := DllCall("LoadImage", "Ptr", 0, "Str", path, "UInt", 1, "Int", 0, "Int", 0, "UInt", 0x10, "Ptr")
        else
            hIcon := path
        SendMessage(0x80, 0, hIcon, this.hwnd) ; WM_SETICON ICON_SMALL
        SendMessage(0x80, 1, hIcon, this.hwnd) ; WM_SETICON ICON_BIG
        return this
    }

    /**
     * Bind Esc to destroying this dialog.
     * @returns  this (chainable)
     */
    esc_to_close() {
        HotIfWinActive("ahk_id " this.hwnd)
        Hotkey("Escape", (*) => this.destroy())
        HotIfWinActive()
        return this
    }

    ctrl_c_to_copy_msg() {
        HotIfWinActive("ahk_id " this.hwnd)
        Hotkey("^c", (*) => this._copy_msg())
        HotIfWinActive()
        return this
    }

    _copy_msg() {
        A_Clipboard := this.msg
        a2tip('Message copied to clipboard!')
    }

    /**
     * Register a handler for the Gui Close event (X button / Alt-F4).
     *
     * @param {Func} fn
     * Callback receiving the Gui object
     * @returns  this (chainable)
     */
    on_close(fn) {
        this._on_close_fn := fn
        this.gui.OnEvent("Close", fn)
        return this
    }

    /**
     * Register a handler for the Gui Escape event.
     *
     * @param {Func} fn
     * Callback receiving the Gui object
     * @returns  this (chainable)
     */
    on_escape(fn) {
        this.gui.OnEvent("Escape", fn)
        return this
    }

    /**
     * Destroy the window and clean up all registered button HWNDs.
     * Safe to call more than once.
     */
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
        if this._exit_on_close
            ExitApp()
    }

    /**
     * Mark this dialog so that destroy() calls ExitApp() after cleanup.
     * Use in standalone example/tool scripts where the dialog is the whole app.
     * For embedded dialogs just call destroy() directly.
     * @returns  this (chainable)
     */
    exit_on_close() {
        this._exit_on_close := true
        ; this.gui.OnEvent("Close", (*) => ExitApp())
        return this
    }
}

/**
 * Register a button control as owner-drawn with custom colors.
 * Call after AddButton. Works before or after Gui.Show().
 *
 * @param {Ctrl} ctrl
 * The button control returned by Gui.AddButton()
 * @param {String} [bg]
 * Background color, 6-digit RRGGBB hex
 * @param {String} [fg]
 * Foreground (text) color, 6-digit RRGGBB hex
 */
a2dlg_make_button(ctrl, bg := "", fg := "") {
    _a2dlg_init()
    global _flat_buttons
    hwnd := ctrl.Hwnd
    ; Register FIRST - WM_DRAWITEM can fire synchronously during the style change below
    _flat_buttons[hwnd] := { bg: bg, fg: fg, text: ctrl.Text }
    ; Switch style bits to BS_OWNERDRAW (0xB), keeping all other flags
    style := DllCall("GetWindowLongPtr", "Ptr", hwnd, "Int", -16, "Ptr")
    DllCall("SetWindowLongPtr", "Ptr", hwnd, "Int", -16, "Ptr", (style & ~0xF) | 0xB)
    ; Synchronous full repaint - button never flashes with the default look
    DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
    DllCall("UpdateWindow", "Ptr", hwnd)
}

/**
 * Return the standard a2 color scheme object.
 *
 * @param {Boolean} dark
 * True for the dark palette, false for light
 * @returns  Object with keys: bg, text, sub, sep, ok, warn, err, btn_bg, acc_fg
 */
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

/**
 * Apply a dark or light DWM title bar (Windows 10 1809+ / Windows 11).
 *
 * @param {Integer} hwnd
 * Window handle
 * @param {Boolean} dark
 * True for dark title bar, false for light
 */
a2dlg_apply_dark_title_bar(hwnd, dark) {
    val := dark ? 1 : 0
    try DllCall("dwmapi\DwmSetWindowAttribute",
        "Ptr", hwnd, "UInt", 20, "Int*", val, "UInt", 4)
}

/**
 * one-time library initializer - called lazily from a2dlg_make_button / A2Dialog.__New
 * No top-level executable code: the library is safe to #Include <a2dlg> without warnings.
 */
_a2dlg_init() {
    static _done := false
    if _done
        return
    _done := true
    global _flat_buttons, _flat_btn_hover
    _flat_buttons := Map()
    _flat_btn_hover := 0
    OnMessage(0x2B, _flat_btn_on_draw)        ; WM_DRAWITEM
    OnMessage(0x200, _flat_btn_on_mouse_move)  ; WM_MOUSEMOVE
    OnMessage(0x2A3, _flat_btn_on_mouse_leave) ; WM_MOUSELEAVE
}

; ================================================================
;  Internal - WM_DRAWITEM handler and GDI helpers
; ================================================================

/**
 * WM_DRAWITEM handler - called by Windows whenever a registered button needs painting.
 * DRAWITEMSTRUCT offsets (x64):
 *   0  CtlType (UInt)   4  CtlID   8  itemID   12 itemAction
 *  16  itemState (UInt) 20 (pad)  24  hwndItem (Ptr)   32  hDC (Ptr)
 *  40  rcItem.left  44  .top  48  .right  52  .bottom  (all Int)
 */
_flat_btn_on_draw(wParam, lParam, *) {
    global _flat_buttons
    if (NumGet(lParam, 0, "UInt") != 4)     ; CtlType must be ODT_BUTTON = 4
        return
    hwnd := NumGet(lParam, 24, "Ptr")
    if !_flat_buttons.Has(hwnd)
        return

    spec := _flat_buttons[hwnd]
    state := NumGet(lParam, 16, "UInt")
    hDC := NumGet(lParam, 32, "Ptr")

    ; Full button bounding rect from DRAWITEMSTRUCT.rcItem
    rc := Buffer(16)
    NumPut("Int", NumGet(lParam, 40, "Int"), rc, 0)    ; left
    NumPut("Int", NumGet(lParam, 44, "Int"), rc, 4)    ; top
    NumPut("Int", NumGet(lParam, 48, "Int"), rc, 8)    ; right
    NumPut("Int", NumGet(lParam, 52, "Int"), rc, 12)    ; bottom

    ; Fill background: darken when pressed, lighten when hovered, plain otherwise
    ; disabled := (state & 0x20)
    disabled := !DllCall("IsWindowEnabled", "Ptr", hwnd)
    bg := disabled ? _flat_btn_disabled(spec.bg)
        : (state & 0x1) ? _flat_btn_dim(spec.bg)
            : (_flat_btn_hover = hwnd) ? _flat_btn_lit(spec.bg)
                : spec.bg
    hBrush := DllCall("CreateSolidBrush", "UInt", _flat_btn_gdi(bg), "Ptr")
    DllCall("FillRect", "Ptr", hDC, "Ptr", rc, "Ptr", hBrush)
    DllCall("DeleteObject", "Ptr", hBrush)

    ; Draw label - dim fg when disabled
    hFont := SendMessage(0x31, 0, 0, hwnd)
    old_font := DllCall("SelectObject", "Ptr", hDC, "Ptr", hFont, "Ptr")
    DllCall("SetBkMode", "Ptr", hDC, "Int", 1)
    fg := disabled ? _flat_btn_disabled(spec.fg) : spec.fg
    DllCall("SetTextColor", "Ptr", hDC, "UInt", _flat_btn_gdi(fg))
    DllCall("DrawTextW", "Ptr", hDC, "WStr", spec.text, "Int", -1,
        "Ptr", rc, "UInt", 0x25)
    DllCall("SelectObject", "Ptr", hDC, "Ptr", old_font)

    ; Dotted focus ring when the button has keyboard focus (ODS_FOCUS = 0x10)
    if (!disabled && (state & 0x10)) {
        inner := Buffer(16)
        NumPut("Int", NumGet(rc, 0, "Int") + 3, inner, 0)
        NumPut("Int", NumGet(rc, 4, "Int") + 3, inner, 4)
        NumPut("Int", NumGet(rc, 8, "Int") - 3, inner, 8)
        NumPut("Int", NumGet(rc, 12, "Int") - 3, inner, 12)
        DllCall("DrawFocusRect", "Ptr", hDC, "Ptr", inner)
    }
    return true
}

/**
 * Convert a 6-digit RRGGBB hex string to a Win32 COLORREF (0x00BBGGRR).
 *
 * @param {String} hex  6-digit RRGGBB hex string
 * @returns  Integer COLORREF value
 */
_flat_btn_gdi(hex) {
    r := Integer("0x" SubStr(hex, 1, 2))
    g := Integer("0x" SubStr(hex, 3, 2))
    b := Integer("0x" SubStr(hex, 5, 2))
    return r | (g << 8) | (b << 16)
}

/**
 * Darken each RGB channel by 30 (clamped to 0) - pressed-state visual feedback.
 *
 * @param {String} hex  6-digit RRGGBB hex string
 * @returns  Darkened 6-digit RRGGBB hex string
 */
_flat_btn_dim(hex) {
    r := Max(0, Integer("0x" SubStr(hex, 1, 2)) - 30)
    g := Max(0, Integer("0x" SubStr(hex, 3, 2)) - 30)
    b := Max(0, Integer("0x" SubStr(hex, 5, 2)) - 30)
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

/**
 * Lighten each RGB channel by 15 (clamped to 255) - hover-state visual feedback.
 *
 * @param {String} hex  6-digit RRGGBB hex string
 * @returns  Lightened 6-digit RRGGBB hex string
 */
_flat_btn_lit(hex) {
    r := Min(255, Integer("0x" SubStr(hex, 1, 2)) + 15)
    g := Min(255, Integer("0x" SubStr(hex, 3, 2)) + 15)
    b := Min(255, Integer("0x" SubStr(hex, 5, 2)) + 15)
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

/**
 * Blend each RGB channel 50% toward mid-grey - disabled-state visual feedback.
 *
 * @param {String} hex  6-digit RRGGBB hex string
 * @returns  Muted 6-digit RRGGBB hex string
 */
_flat_btn_disabled(hex) {
    r := Integer("0x" SubStr(hex, 1, 2))
    g := Integer("0x" SubStr(hex, 3, 2))
    b := Integer("0x" SubStr(hex, 5, 2))
    ; Blend 50% toward mid-grey (128, 128, 128)
    r := (r + 128) // 2
    g := (g + 128) // 2
    b := (b + 128) // 2
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

/**
 * WM_MOUSEMOVE - fires on the button control; starts leave-tracking if not already active.
 * TRACKMOUSEEVENT layout (x64): cbSize DWORD@0, dwFlags DWORD@4, hwndTrack Ptr@8, dwHoverTime DWORD@16
 */
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

/**
 * WM_MOUSELEAVE - fires on the button that called TrackMouseEvent when the cursor leaves.
 */
_flat_btn_on_mouse_leave(wParam, lParam, msg, hwnd) {
    global _flat_buttons, _flat_btn_hover
    if _flat_btn_hover = hwnd
        _flat_btn_hover := 0
    if _flat_buttons.Has(hwnd) {
        DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
        DllCall("UpdateWindow", "Ptr", hwnd)
    }
}

; ================================================================
;  Popup dialog functions
;
;   a2dlg_info(msg [, title])                    - info message + OK
;   a2dlg_error(msg [, title, error_detail])     - error + selectable detail + OK
;   a2dlg_yes_no(msg [, title])                  => true / false
;   a2dlg_ok_cancel(msg [, title])               => true / false
;   a2dlg_input(msg [, title, default_text])     => "" (cancelled) or user string
;
;  All functions block until the user dismisses the dialog.
; ================================================================

/**
 * Show a blocking informational popup with an OK button.
 * @example
 *      a2dlg_info("Operation complete.", "Done")
 *
 * @param {String} msg
 * Message text
 * @param {String} title
 * Window title (default "a2 Information")
 * @param {Boolean} dark
 * Force dark/light theme; omit to follow the system setting
 */
a2dlg_info(msg, title := "a2 Information", dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "ℹ️", "ok", 380, dark, &center_on_window)
    dlg.msg := msg
    dlg.ctrl_c_to_copy_msg()
    dlg.btn_ok()
    _a2dlg_resolve(dlg, center_on_window)
}

/**
 * Show a blocking error popup with an optional selectable detail box and OK button.
 * @example
 *      a2dlg_error("Something went wrong.", "Error", "Traceback line 1`nLine 2")
 *
 * @param {String} msg
 * Message text
 * @param {String} title
 * Window title (default "a2 Error")
 * @param {String} error_detail
 * Optional selectable detail text shown in a read-only code box
 * @param {Boolean} dark
 * Force dark/light theme; omit to follow the system setting
 */
a2dlg_error(msg, title := "a2 Error", error_detail := "", dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "❌", "warn", 420, dark, &center_on_window)
    dlg.msg := msg

    if (error_detail != "") {
        dlg.code_box(error_detail)
        dlg.msg .= "`n" error_detail
    }
    dlg.ctrl_c_to_copy_msg()
    dlg.space(6)
    dlg.sep()
    dlg.btn_ok(, , , bg := dlg.c.err, fg := "F8F8F8")
    _a2dlg_resolve(dlg, center_on_window)
}

/**
 * Show blocking question dialog with Yes / No buttons.
 * @example
 *      if a2dlg_yes_no("Delete this item?")
 *          delete_item()
 *
 * @param {String} msg
 * Question text.
 * @param {String} [title="a2"]
 * Optional Window title.
 * @param {Boolean} [dark]
 * Optional Force dark/light theme; omit to follow the system setting.
 * @returns  true (Yes) / false (No or closed)
 */
a2dlg_yes_no(msg, title := "a2 Yes/No", dark := -1, center_on_window := 0) {
    return _a2dlg_confirm(msg, title, "Yes", "No", dark, center_on_window)
}

/**
 * Show blocking confirmation dialog with OK / Cancel buttons.
 * @example
 *      if a2dlg_ok_cancel("Proceed with installation?")
 *          install()
 *
 * @param {String} msg
 * Confirmation text.
 * @param {String} [title="a2"]
 * Optional Window title.
 * @param {Boolean} [dark]
 * Optional Force dark/light theme; omit to follow the system setting.
 * @returns {Boolean} true (OK) / false (Cancel or closed)
 */
a2dlg_ok_cancel(msg, title := "a2 OK/Cancel", dark := -1, center_on_window := 0) {
    return _a2dlg_confirm(msg, title, "OK", "Cancel", dark, center_on_window)
}

/**
 * Show a blocking text-input dialog.
 * @example
 *      name := a2dlg_input("Enter your name:", "Name", "World")
 *
 * @param {String} msg
 * Prompt text shown above the input field
 * @param {String} [title]
 * Window title (default "a2 Input")
 * @param {String} [default_text]
 * Pre-filled value in the edit field
 * @param {Boolean} [dark]
 * Force dark/light theme; omit to follow the system setting
 * @returns {String} Entered string, or "" if cancelled
 */
a2dlg_input(msg, title := "a2 Input", default_text := "", dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "✏️", "ok", 380, dark, &center_on_window)
    edit := dlg.edit_field(default_text)
    dlg.space(6)
    dlg.sep()
    dlg.result := default_text
    dlg.btn_ok_cancel(, () => dlg.result := edit.Value)
    edit.Focus()
    _a2dlg_resolve(dlg, center_on_window)
    return dlg.cancelled ? "" : dlg.result
}

/**
 * Add a large colored icon glyph + wrapped message body to a dialog.
 *
 * @param {A2Dialog} dlg
 * Target dialog
 * @param {String} icon_glyph
 * Emoji / glyph rendered large on the left
 * @param {String} icon_color
 * 6-digit RRGGBB hex color for the glyph
 * @param {String} msg
 * Message text (wraps automatically)
 * @returns  Text ctrl for the message body
 */
_a2dlg_icon_msg(dlg, icon_glyph, icon_color, msg) {
    inner_w := dlg.width - dlg.pad * 2
    ; Icon - large, colored
    dlg.gui.SetFont("s18 w700 c" icon_color, dlg.font_face)
    dlg.gui.AddText("x" dlg.pad " y" dlg.height " w30 h30 Center", icon_glyph)
    ; Message - wrap within remaining width
    dlg.gui.SetFont("s" dlg.font_size " w400 c" dlg.c.text, dlg.font_face)
    msg_x := dlg.pad + 36
    msg_w := inner_w - 36
    msg_ctrl := dlg.gui.AddText("x" msg_x " y" dlg.height " w" msg_w " Wrap", msg)
    msg_ctrl.GetPos(, , , &mh)
    dlg.space(Max(34, mh + 4))
    return msg_ctrl
}

_a2dlg_make(title, msg, glyph, glyph_color, w, dark := -1, &center_on_window := 0) {
    if (center_on_window == 1)
        center_on_window := WinExist('A')
    opts := { w: w, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if dark != -1
        opts.dark := dark
    dlg := A2Dialog(title, opts)
    dlg.space(4)
    ; TODO: this should work with glyph_row right away!
    ; row := dlg.glyph_row(glyph, msg, dlg.c.%glyph_color%)
    ; dlg.set_color(dlg.c.text, row.text)
    _a2dlg_icon_msg(dlg, glyph, dlg.c.%glyph_color%, msg)
    dlg.space(4)
    dlg.sep()
    return dlg
}

_a2dlg_resolve(dlg, center_on_window) {
    dlg.esc_to_close()
    if center_on_window != 0
        dlg.show(,center_on_window)
    else
        dlg.show()
    WinWaitClose("ahk_id " dlg.hwnd)
}

_a2dlg_confirm(msg, title, ok_label, cancel_label, dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "❓", "warn", 380, dark, &center_on_window)
    dlg.msg := msg
    dlg.ctrl_c_to_copy_msg()
    dlg.btn_ok_cancel(, , ok_label, cancel_label)
    _a2dlg_resolve(dlg, center_on_window)
    return !dlg.cancelled
}
