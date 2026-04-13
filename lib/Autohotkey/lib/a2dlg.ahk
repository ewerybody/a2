/************************************************************************
 * a2dlg.ahk - reusable dialog helpers for a2
 * High-level (A2Dialog class):
 *   dlg := A2Dialog(title [, opts])            - opts: w, pad, flags, dark, font: {face, size}
 *   dlg.header(text [, icon_path])             - large title with optional 32px icon
 *   dlg.sep()                                  - thin horizontal separator line
 *   dlg.glyph_row(icon, text [,color, subtext])- colored icon + label row => {icon, text}
 *   dlg.row_pending([icon, text])              - muted row for live update => {icon, text}
 *   dlg.text(content [, color, ahk_opts])      - small caption / status line => ctrl
 *   dlg.space(px)                              - extra vertical gap
 *   dlg.btn(label, [bg, fg , ahk_opts])        - single flat button => ctrl
 *   dlg.btn_row(specs [w, h, gap, func])       - left-aligned button row => [controls]
 *   dlg.btn_row_right(specs [w, h, gap, fund]) - right-aligned footer row => [controls]
 *  Per-button width override: add w to a spec, e.g. {label: "X", bg:…, fg:…, w: 120}
 *   dlg.show([extra_h], [center_on_window])    - first show, centered on screen or on
 *                                                window of given handle.
 *   dlg.resize([extra_h])                      - resize in-place (progressive reveal)
 *   dlg.set_icon(path)                         - set window title-bar / taskbar icon
 *   dlg.esc_to_close()                         - Set Esc to close.
 *   dlg.on_close(fn)                           - register Gui Close handler
 *   dlg.destroy()                              - destroy window and clean up btn registry
 *   dlg.gui  dlg.hwnd  dlg.c  dlg.dark         - direct access to underlying objects
 *  Button specs (for btn_row / btn_row_right): array of {label, bg, fg [, opts]}
 *    opts: extra AHK button option string, e.g. "Default"
 *  Color strings are always 6-digit "RRGGBB" hex (no #).
 *  Include this file once per script - it self-registers the WM_DRAWITEM handler.
 ***********************************************************************/
#Include <a2tip>
#Include <a2icon>
#Include <i18n>
#Include <theme>
#Include <string>
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
    font_weight_normal := 400
    font_weight_bold := 600
    font_weight_heavy := 700

    _icon := ""
    a2_icon := A2Icons.a2

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
     *      dlg := A2Dialog("My Dialog", {w: 400})
     *
     * @param {(String)} title - Dialog Window title.
     * @param {(Object)} opts - Options: {w, pad, flags, theme, dark, font: {face, size}}
     */
    __New(title, opts := {}) {
        _a2dlg_init()
        ; Padding value for spacing.
        this.pad := opts.HasProp("pad") ? opts.pad : 14
        this.gap := opts.HasProp("gap") ? opts.gap : 8
        ; Total height of the dialog.
        this.height := this.pad
        ; Total width of the dialog.
        this.width := opts.HasProp("w") ? opts.w : 480
        ; Theme mode. `dark` false is "light".
        this.dark := opts.HasProp("dark") ? opts.dark : theme_is_dark()
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

        this._t := i18n_domain('general')
    }

    /** Read-only HWND of the underlying Gui. */
    hwnd => this.gui.Hwnd

    ; Content builders:  (most return `this` for optional chaining)

    /**
     * Large title line with icon to the left.
     * @param {(String)} text - Title text to display.
     * @param {(String)} [icon_path] - Optional icon file path; supports "file,N" registry format.
     * @param {(Integer)} [icon_size] - Optional icon size (Default: 32x32px).
     * @returns  this (chainable)
     */
    header(text, icon_path := "", icon_size := 32) {
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
        this.gui.SetFont("s" (this.font_size + 2) " w" this.font_weight_heavy " c" this.c.text, this.font_face)
        if (icon_file && FileExist(icon_file)) {
            try {
                pic_ctrl := this.gui.AddPicture("x" pad " y" y " w" icon_size " h" icon_size " " icon_opt, icon_file)
                pic_ctrl.GetPos(,, &pic_width, &pic_height)
            } catch
                pic_width := 0, pic_height := 0
            txt_ctrl := this.gui.AddText("x" (pad + pic_width + this.gap) " y" (y + this.gap) " w" (this.width - pad - pic_width - pad), text)
        } else {
            pic_height := 0
            txt_ctrl := this.gui.AddText("x" pad " y" (y + this.gap / 2) " w" (this.width - pad * 2), text)
        }
        this.space(Max(_a2dlg_get_height(txt_ctrl), pic_height) + this.pad)
        return this
    }

    /**
     * Add a thin horizontal separator line followed by a small gap.
     * @returns  this (chainable)
     */
    sep() {
        this.gui.SetFont("s1")
        x := this.gui.AddText("x0 y" this.height " w" this.width " h1 Background" this.c.sep)
        this.space(10)
        return this
    }

    /**
     * Colored icon glyph + main label + optional smaller subtext below.
     * @param {(String)} glyph - Glyph or emoji for the first column.
     * @param {(String)} text - Main label text.
     * @param {(String)} [color] - Optional 6-digit RRGGBB hex color for the icon
     * @param {(String)} [subtext] - Optional muted line below the label
     * @param {(Object)} [opts] - Optional options {
     *  active: {Boolean} to dim the control on creation.,
     *  glyph_color: {String} extra color for the glyph if it should be different.,
     *  glyph_size: {Integer} extra size to make the glyph appear bigger or smaller
     *  }
     * @returns  {glyph: ctrl, text: ctrl, items: [glyph_ctrl, text_ctrl]} - either can be updated later
     */
    glyph_row(glyph, text, color := "", subtext := "", opts := {}) {
        if !color
            color := this.c.text
        pad := this.pad
        y := this.height

        glyph_size := opts.HasProp("glyph_size") ? opts.glyph_size : this.font_size + 1
        em_px := Round(glyph_size * A_ScreenDPI / 72)
        glyph_box := em_px + 2
        glyph_color := opts.HasProp("glyph_color") ? opts.glyph_color : color
        this.gui.SetFont("s" glyph_size " w" this.font_weight_normal " c" glyph_color, this.font_face)
        glyph_ctrl := this.gui.AddText("x" pad " y" y " w" glyph_box " h" glyph_box " Center", glyph)
        ; Store color so we can toggle without needing the color scheme
        glyph_ctrl.color_on := glyph_color
        if opts.HasProp("active") and !opts.active
            glyph_ctrl.SetFont("c" this.c.sub)

        this.gui.SetFont("s" this.font_size " w" this.font_weight_normal " c" color, this.font_face)
        msg_x := pad * 2 + glyph_box
        msg_w := this.width - pad - msg_x
        text_ctrl := this.gui.AddText("x" msg_x " y" y " w" msg_w " Wrap", text)
        text_ctrl.color_on := color
        this.space(Max(_a2dlg_get_height(glyph_ctrl), _a2dlg_get_height(text_ctrl) + 4))

        if subtext {
            this.gui.SetFont("s" (this.font_size - 1) " c" this.c.sub, this.font_face)
            this.gui.AddText("x" msg_x " y" this.height " w" msg_w, subtext)
            this.space(20)
        }
        return { glyph: glyph_ctrl, text: text_ctrl, items: [glyph_ctrl, text_ctrl] }
    }

    /**
     * Restore each control to its original color_on color.
     * Accepts individual controls or glyph_row return values (which have an .items array).
     * @param {Any*} items - Controls or row refs to activate (variadic).
     * @returns  this (chainable)
     */
    set_active(items*) {
        for item in items {
            if item.HasProp('items') {
                for sub_item in item.items
                    if sub_item.HasProp("color_on")
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
     * @param {Any*} items - Controls or row refs to deactivate (variadic).
     * @returns  this (chainable)
     */
    set_inactive(items*) {
        this.set_color(this.c.sub, items*)
        return this
    }

    /**
     * Set each control to an arbitrary color.
     * Accepts individual controls or glyph_row return values (which have an .items array).
     * @param {(String)} color - 6-digit RRGGBB hex color to apply.
     * @param {Any*} items - Controls or row refs to recolor (variadic).
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
     * Arrange a list of controls to the right border of the dialog.
     * @param {(Array[Control])} controls - Array for control objects to shift to the right.
     */
    align_right(controls) {
        ; get right-most gap and add it to each of the controls
        controls[-1].GetPos(&last_x,, &last_w)
        shift := this.width - last_x - last_w - this.pad
        if shift <= 0
            return controls

        for i, ctrl in controls {
            ctrl.GetPos(&x)
            ctrl.Move(x + shift)
        }
        return controls
    }

    /**
     * @private Assemble positioning statement to manage x/y and width of a new control.
     * @param {(Control)} ctrl - Gui-control object to align on. x: ctrl.x+w+gap; y: ctrl.y
     * When empty: use default positioning x : left most after pad; y: this.height
     * @param {(String)} [new_type] - Actually just for the error message in case.
     * @param {(String)} [pos_opts] - Additional AHK Control options to pass along.
     * @param {(Boolean)} max_width - Set `w` width argument to take all or rest of
     * horizontal space available in dialog (Default: false).
     * @returns {(Object)} {opts, x, y, w}
     */
    _align_next_to(ctrl, new_type := "", pos_opts := "", max_width := false) {
        if (ctrl == "") {
            w := max_width ? this.width - this.pad * 2 : 0
            opts := "x" this.pad " y" this.height " " (max_width ? " w" w " " : "") pos_opts
            return {opts: opts, x: this.pad, y: this.height, w: w}
        }
        ctrl.GetPos(&last_x, &last_y, &last_w)
        last_right := last_x + last_w + this.gap
        if last_right > this.width
            throw Error(
                'Placing this "' new_type '" next to given control`n'
                '  type: ' Type(ctrl) ' x: ' last_x ' w: ' last_w '`n'
                'will put it outside of the dialogs width (' this.width ')!'
            )
        w := this.width - last_x - last_w - this.pad * 2
        x := last_x + last_w + this.gap
        opts := "x" x " y" last_y " " (max_width ? " w" w " " : "") pos_opts
        return {opts: opts, x: x, y: this.height, w: w}
    }

    /**
     * Bold sub-section heading (font_size+1, text color).
     * @param {(String)} text - Heading text to display.
     * @returns  Text ctrl
     */
    heading(text) {
        pad := this.pad
        this.gui.SetFont("s" (this.font_size + 1) " w" this.font_weight_heavy " c" this.c.text, this.font_face)
        ctrl := this.gui.AddText("x" pad " y" this.height " w" (this.width - pad * 2), text)
        this.space(24)
        return ctrl
    }

    /**
     * Small muted caption. Wraps and auto-sizes to the rendered height.
     * @param {(String)} content - Text to display.
     * @param {(String)} ahk_opts - Extra AHK control option string appended to the AddText call.
     * @returns  Text ctrl
     */
    text(content, color := "", ahk_opts := "") {
        if !color
            color := this.c.sub
        pad := this.pad
        ; prepend options with space if any
        opts := ahk_opts ? " " ahk_opts : ""
        this.gui.SetFont("s" (this.font_size - 1) " c" color, this.font_face)
        ctrl := this.gui.AddText("x" pad " y" this.height " w" (this.width - pad * 2) " Wrap" opts, content)
        this.space(_a2dlg_get_height(ctrl) + 6)
        return ctrl
    }

    /**
     * Small left aligned text label.
     * @param {(String)} text - Text to display.
     * @param {(String)} color - 6-digit RRGGBB hex color to apply.
     * @param {(String)} ahk_opts - Extra AHK control option string appended to the AddText call.
     * @returns  Text ctrl
     */
    label(text, color := "", ahk_opts := "", next_to := "") {
        if !color
            color := this.c.text
        opts := ahk_opts ? " " ahk_opts : ""
        pos := this._align_next_to(next_to, 'Text', ahk_opts)
        this.gui.SetFont("s" this.font_size " c" color, this.font_face)
        ctrl := this.gui.AddText(pos.opts, text)
        this.space(_a2dlg_get_height(ctrl) + 6)
        return ctrl
    }

    /**
     * Picture on the left + wrapped sub-text on the right.
     * @param {(String)} file - Path to the image or executable file.
     * @param {(String)} opt - Extra AHK picture option string (e.g. "Icon3"), or "".
     * @param {(String)} text - Caption text displayed to the right of the picture.
     * @returns  {pic: ctrl, text: ctrl} - pic is "" if the file is missing
     */
    pic_row(pic_path, opt, text, size := 22) {
        pad := this.pad
        y := this.height
        pic_ctrl := ""
        if (pic_path && FileExist(pic_path)) {
            try
                pic_ctrl := this.gui.AddPicture("x" pad " y" y " w" size " h" size " " opt, pic_path)
            catch
                pic_ctrl := this.gui.AddPicture("x" pad " y" y " w" size " h" size " " opt, A2Icons.a2x)
        }
        this.gui.SetFont("s" (this.font_size - 1) " c" this.c.sub, this.font_face)
        txt_ctrl := this.gui.AddText("x" (pad + 28) " y" (y + 4)
        " w" (this.width - pad * 2 - 28) " Wrap", text)
        this.space(Max(28, _a2dlg_get_height(txt_ctrl) + 8))
        return { pic: pic_ctrl, text: txt_ctrl }
    }

    /**
     * Lay out array of pictures in a horizontal strip, auto-clipped to content width.
     * @param {(Array)} items - Array of paths, or objects with {file [, opt]} for extra AHK picture options.
     * @param {(Integer)} [size] - Width and height of each picture in pixels (Default: 32).
     * @param {(Integer)} [gap] - Spacing between pictures in pixels (Default: 8).
     * @returns {(Integer)} Count of pictures actually shown.
     */
    pic_strip(items, size := 32, gap := "") {
        gap := gap == "" ? this.gap : gap
        slot := size + gap
        n := Min(items.Length, (this.width - this.pad * 2 + gap) // slot)
        loop n {
            item := items[A_Index]
            file_path := (item is String) ? item : item.file
            opt := (item is String || !item.HasProp("opt")) ? "" : item.opt
            try this.gui.AddPicture("x" (this.pad + (A_Index - 1) * slot) " y" this.height
            " w" size " h" size " " opt, file_path)
        }
        this.space(size + 4)
        return n
    }

    /**
     * Add extra vertical whitespace.
     * @param {(Integer)} [gap] - Pixels to advance (Default: dialog gap 8).
     * @returns  this (chainable)
     */
    space(gap := "") {
        gap := (gap = "") ? this.gap : gap
        this.height += gap
        return this
    }

    ; Buttons

    /**
     * @private  Create, style, and register one flat button.
     * @param {(Object)} spec - {label, [bg, fg, opts, func]} `w` and `h` in here are ignored!
     * @param {(String)} pos_opts - AHK position/size string built by the caller.
     * @returns Button ctrl
     */
    _btn_one(spec, pos_opts, next_to := "") {
        bg    := spec.HasProp("bg")   && spec.bg   ? spec.bg   : this.c.btn_bg
        fg    := spec.HasProp("fg")   && spec.fg   ? spec.fg   : this.c.text
        extra := spec.HasProp("opts") && spec.opts ? " " spec.opts : ""
        pos := this._align_next_to(next_to, 'Button', pos_opts)
        ctrl  := this.gui.AddButton(pos.opts extra, spec.label)
        a2dlg_make_button(ctrl, bg, fg)
        this._btn_hwnds.Push(ctrl.Hwnd)
        if spec.HasProp("func") && spec.func != ""
            ctrl.OnEvent("Click", spec.func)
        return ctrl
    }

    /**
     * Single flat button placed with a raw AHK option string.
     * Use btn_row / btn_row_right for grouped layouts.
     * @param {(String)} label - Button label text.
     * @param {(Function)} [func] - To bind to function directly.
     * @param {(Integer)} [w] - Button width in pixels; 0 = auto-size each to its label (Default: 0).
     * @param {(Integer)} [h] - Button height in pixels (Default: 30).
     * @param {(String)} [bg] - Optional Background color, 6-digit RRGGBB hex.
     * @param {(String)} [fg] - Optional Foreground (text) color, 6-digit RRGGBB hex.
     * @param {(String)} [ahk_opts] - Optional AHK button option string (e.g. "x10 y20 w80 h28").
     * @returns Button ctrl
     */
    btn(label, func := "", w := 0, h := 28, bg := "", fg := "", ahk_opts := "", next_to := "") {
        this.gui.SetFont("s" this.font_size " w" this.font_weight_bold, this.font_face)
        ahk_opts := (w ? "w" w " " : "") (h ? "h" h " " : "") ahk_opts
        new_btn := this._btn_one({label: label, bg: bg, fg: fg, func: func}, ahk_opts, next_to)
        this.height := _a2dlg_get_bottom(new_btn)
        return new_btn
    }

    /**
     * Horizontal row of flat buttons,
     * Distributed across width (w:=-1) or left-aligned from left margin (w:=0/N).
     * @param {Array} specs - Array of {`label`, [`bg`, `fg` , `opts`, `func`]}
     * Optional. For colors: `bg`, `fg`, `opts` for extra AHK button option string.
     * `func` to bind to function directly.
     * @param {(Integer)} [w] - Set buttons width in pixels.
     *  0 = Do nothing, auto-size each to its own label.
     * -1 = Distribute all evenly across width of dialog.
     *  N = Dedicated width of N pixels for all buttons. (Default: -1).
     * @param {(Integer)} [h] - Button height in pixels (Default: 30).
     * @param {(Integer)} [gap] - Spacing between buttons in pixels (Default: 8)
     * @returns  Array of button controls in spec order.
     */
    btn_row(specs, w := -1, h := 30, gap := 8) {
        this.gui.SetFont("s" this.font_size " w" this.font_weight_bold, this.font_face)
        ; Resolve distribute mode: available width minus any explicit spec.w slots
        if w = -1 {
            fixed_total := 0
            n_auto := 0
            for spec in specs {
                if spec.HasProp("w")
                    fixed_total += spec.w
                else
                    n_auto++
            }
            dist_w := n_auto ? (this.width - this.pad * 2 - gap * (specs.Length - 1) - fixed_total) // n_auto : 0
        }

        controls := []
        for i, spec in specs {
            ; width is spec.w if present, otherwise auto width or one for all
            this_w := spec.HasProp("w") ? spec.w : (w = -1) ? dist_w : w
            x_opt := (i = 1) ? "x" this.pad " y" this.height : "x+" gap " yp"
            pos_opts   := x_opt (this_w ? " w" this_w : "") " h" h
            controls.Push(this._btn_one(spec, pos_opts))
        }
        this.space(h + gap)
        return controls
    }

    /**
     * Horizontal row of flat buttons, right-aligned - typical footer layout.
     * @param {Array} specs - Array of {label, bg, fg [, opts, w]}
     * `opts`: extra AHK option string; w: per-button width in pixel.
     * @param {(Integer)} [w] - Set buttons width in pixels.
     *  0 = Do nothing, auto-size each to its own label.
     * -1 = Distribute all evenly across width of dialog.
     *  N = Dedicated width of N pixels for all buttons. (Default: 0).
     * @param {(Integer)} [h] - Button height in pixels (Default: 30).
     * @param {(Integer)} [gap] - Spacing between buttons in pixels (Default: 8).
     * @returns  Array of button controls in left => right order
     */
    btn_row_right(specs, w := 0, h := 30, gap := 8) {
        this.gui.SetFont("s" this.font_size " w" this.font_weight_bold, this.font_face)
        controls := this.btn_row(specs, w, h, gap)
        if w = -1
            return controls
        this.align_right(controls)
        return controls
    }

    /**
     * Add a right-aligned "Close" button that calls destroy().
     * Sets cancelled := false - closing is not cancelling.
     * @returns  this (chainable)
     */
    btn_close() {
        this.btn_row_right([{ label: this._t['close'], w:100, bg: this.c.btn_bg, opts: "Default" }])[1]
        .OnEvent("Click", (*) => (this.cancelled := false, this.destroy()))
    }

    /**
     * Add a right-aligned OK + Cancel button pair.
     * OK sets cancelled := false and calls destroy(); Cancel just calls destroy().
     * @param {(Integer)} [bw=80] - Uniform button width in pixels.
     * @param {(Func)} [on_ok] - Optional callback fired before destroy on OK
     * @param {(String)} [ok_label] - Label override for the OK button (Default: "OK").
     * @param {(String)} [cancel_label] - Label override for the Cancel button (Default: "Cancel").
     * @param {(Boolean)} [default_btn] - Whether OK gets the Default (Enter key) style.
     * @returns  Array[ok_ctrl, cancel_ctrl]
     */
    btn_ok_cancel(bw := 80, on_ok := "", ok_label := "", cancel_label := "", default_btn := true) {
        ok_label := ok_label ? ok_label : "OK"
        cancel_label := cancel_label ? cancel_label : this._t['cancel']
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
     * @param {(Integer)} [bw] - Button width in pixels (Default: 80).
     * @param {(Func)} [on_ok] - Optional callback fired before destroy.
     * @param {(String)} [ok_label] - Label override for the OK button (Default: "OK").
     * @param {(String)} [bg] - Background color override (Default: c.ok).
     * @param {(String)} [fg] - Foreground color override (Default: c.acc_fg).
     * @param {(Boolean)} [default_btn] - Whether OK gets the Default (Enter key) style.
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
     * @param {(String)} text - Initial content.
     * @param {(Integer)} [h] - Box height in pixels.
     * @returns  Edit ctrl (Value can be updated later)
     */
    code_box(text, h := 64, next_to := "", bottom_line_color := "") {
        this.gui.SetFont("s" (this.font_size - 1) " w" this.font_weight_normal " c" this.c.sub, "Consolas")
        pos := this._align_next_to(next_to, 'Edit',, max_width:=true)
        ctrl := this.gui.AddEdit(pos.opts " h" h " ReadOnly -E0x200 Background" this.c.sub_bg, text)
        bottom_line_color := bottom_line_color ? bottom_line_color : this.c.sep
        this.height := _a2dlg_get_bottom(ctrl)
        this.gui.AddText("x" pos.x " y" this.height " w" pos.w " h1 Background" bottom_line_color)
        this.space()
        return ctrl
    }

    /**
     * Single-line text input with a subtle underline separator below.
     * @param {(String)} [default_text] - Pre-filled value.
     * @returns  Edit ctrl
     */
    edit_field(default_text := "", rows := 1, next_to := "") {
        this.gui.SetFont("s" this.font_size " w" this.font_weight_normal " c" this.c.text, this.font_face)
        pos := this._align_next_to(next_to, 'Edit',, max_width:=true)
        ctrl := this.gui.AddEdit(
            pos.opts " h24 -Border -E0x200 Background" this.c.sub_bg " r" rows,
            default_text
        )
        ; Add a bottom line to the field
        this.height := _a2dlg_get_bottom(ctrl)
        this.gui.AddText("x" pos.x " y" this.height " w" pos.w " h1 Background" this.c.ok)
        this.space()
        return ctrl
    }

    /**
     * Add an arbitrary control to the dialog.
     * @param {(String)} control_type - Control Type name. Such as: ComboBox, Slider, UpDown ..
     * basically anything listed under: https://www.autohotkey.com/docs/v2/lib/GuiControls.htm#toc
     * @param {(String)} [options] - Options string specific to the control.
     * Try to omit `x` and `y` in here! Rather use `next_to`.
     * @param {(Control)} [next_to] - A control to align the new one to.
     * It will be placed at the same height and at the right end.
     * @param {(String)} extra - Extra options for the specific control.
     * That's the "text" for instance at a "Text" control.
     * @param {(Boolean)} max_width - Make the control take all or rest of horizontal
     * space available in dialog (Default: false).
     */
    add(control_type, options := "", next_to := "", extra := "", max_width := false) {
        pos := this._align_next_to(next_to, control_type,, max_width)
        ctrl := this.gui.Add(control_type, pos.opts options, extra)
        this.height := Max(this.height, _a2dlg_get_bottom(ctrl) + this.gap)
        return ctrl
    }

    /**
     * Custom checkbox with our theme icons.
     * @param {(String)} label - Label text displayed next to the checkbox
     * @param {(Integer)} [checked] - Initial state.
     * @param {(Control)} [next_to] - Optional control to align next to.
     * @param {(Function)} [func] - Optional function to call on state change.
     * @returns Checkbox control
     */
    checkbox(label, checked := 0, next_to := "", func := "") {
        pos := this._align_next_to(next_to, "CheckBox")
        size := this.font_size + 10  ; scale with font
        icon_on := A2Icons.checkbox_on, icon_off := A2Icons.checkbox_off, icon_hover := A2Icons.checkbox_hover
        check_ctrl := this.gui.AddPicture(pos.opts " w" size " h" size, checked ? icon_on : icon_off)
        check_ctrl.checked := checked,
        check_ctrl.icon_on := icon_on,
        check_ctrl.icon_off := icon_off
        check_ctrl.icon_hover := icon_hover
        toggle := (chk, *) => (
            chk.checked := !chk.checked,
            chk.Value := chk.checked ? icon_on : icon_off,
            func ? func(chk.checked) : 0
        )
        check_ctrl.OnEvent("Click", toggle)

        ; +0x100 aka SS_NOTIFY: for better firing the click
        pos_opts := "x" 1 + pos.x + _a2dlg_get_width(check_ctrl) " y" pos.y " +0x100"
        this.gui.SetFont("s" this.font_size " c" this.c.text, this.font_face)
        label_ctrl := this.gui.AddText(pos_opts, " " label)

        label_ctrl.OnEvent("Click", (*) => toggle(check_ctrl))
        check_ctrl.label := label_ctrl

        ; register for hover icon swapping
        global _a2dlg_pic_map
        _a2dlg_pic_map[check_ctrl.Hwnd] := check_ctrl
        _a2dlg_pic_map[label_ctrl.Hwnd] := check_ctrl
        this._btn_hwnds.Push(check_ctrl.Hwnd)
        this._btn_hwnds.Push(label_ctrl.Hwnd)

        this.height := Max(this.height, _a2dlg_get_bottom(check_ctrl) + this.gap)
        return check_ctrl
    }

    ; Window management methods

    /**
     * Display the dialog to the user.
     * @param {(Integer)} [extra_h] - Extra pixels of height to reserve below current content (Default: 0).
     * @param {(Integer)} [center_on_window] - Optional window handle to center the dialog on. (Default 0 > centers on screen).
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
     * @param {(Integer)} extra_h - Extra pixels of height to reserve (Default: 0).
     * @returns  this (chainable)
     */
    resize(extra_h := 0) {
        this.gui.Show("w" this.width " h" (this.height + extra_h) " NA")
        return this
    }

    /**
     * Set the title-bar and taskbar icon.
     * @param {(String|Integer)} path - File path to an ICO/EXE/DLL, or an HICON handle returned by icon_extract().
     * @param {(Integer)} index - Icon index in case a multi icon path is passed like on .exe and .dll
     * @returns  this (chainable)
     */
    set_icon(h_icon, index := "") {
        try_path := index ? h_icon ',' index : h_icon
        if (try_path == this._icon)
            return
        this._icon := try_path

        icon_info := icon_path_split(try_path)
        icon_info.file := path_expand_env(icon_info.file)
        if FileExist(icon_info.file) {
            h_icon := icon_extract(icon_info.file, icon_info.idx)
            if h_icon == 0 {
                ; path := path_expand_env(path)
                h_icon := DllCall("LoadImage", "Ptr", 0, "Str", icon_info.file, "UInt", 1, "Int", 0, "Int", 0, "UInt", 0x10, "Ptr")
            }
        }
        SendMessage(0x80, 0, h_icon, this.hwnd) ; WM_SETICON ICON_SMALL
        SendMessage(0x80, 1, h_icon, this.hwnd) ; WM_SETICON ICON_BIG
        return this
    }

    /**
     * Bind Esc to destroying this dialog.
     * @returns  this (chainable)
     */
    esc_to_close(*) {
        HotIfWinActive("ahk_id " this.hwnd)
        Hotkey("Escape", (*) => this.destroy())
        HotIfWinActive()
        return this
    }

    /**
     * Bind Ctrl+C to copy the dialogs current message.
     * @returns  this (chainable)
     */
    ctrl_c_to_copy_msg(*) {
        HotIfWinActive("ahk_id " this.hwnd)
        Hotkey("^c", (*) => (A_Clipboard := this.msg, a2tip('Message copied to clipboard!')))
        HotIfWinActive()
        return this
    }

    /**
     * Register a handler for the Gui Close event (X button / Alt-F4).
     * @param {Func} fn - Callback receiving the Gui object.
     * @returns  this (chainable)
     */
    on_close(fn) {
        this._on_close_fn := fn
        this.gui.OnEvent("Close", fn)
        return this
    }

    /**
     * Register a handler for the Gui Escape event.
     * @param {Func} fn - Callback receiving the Gui object.
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
    destroy(*) {
        if this._destroyed
            return
        this._destroyed := true
        global _a2dlg_buttons_map, _a2dlg_btn_hover, _a2dlg_pic_map
        for hwnd in this._btn_hwnds {
            if _a2dlg_buttons_map.Has(hwnd)
                _a2dlg_buttons_map.Delete(hwnd)
            if (_a2dlg_btn_hover = hwnd)
                _a2dlg_btn_hover := 0
            if _a2dlg_pic_map.Has(hwnd)
                _a2dlg_pic_map.Delete(hwnd)
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
    exit_on_close(*) {
        this._exit_on_close := true
        return this
    }
}

/**
 * Register a button control as owner-drawn with custom colors.
 * Call after AddButton. Works before or after Gui.Show().
 * @param {(Ctrl)} ctrl - The button control returned by Gui.AddButton().
 * @param {(String)} [bg] - Background color, 6-digit RRGGBB hex.
 * @param {(String)} [fg] - Foreground (text) color, 6-digit RRGGBB hex.
 */
a2dlg_make_button(ctrl, bg := "", fg := "") {
    _a2dlg_init()
    global _a2dlg_buttons_map
    hwnd := ctrl.Hwnd
    ; Register FIRST - WM_DRAWITEM can fire synchronously during the style change below
    _a2dlg_buttons_map[hwnd] := { bg: bg, fg: fg, text: ctrl.Text }
    ; Switch style bits to BS_OWNERDRAW (0xB), keeping all other flags
    style := DllCall("GetWindowLongPtr", "Ptr", hwnd, "Int", -16, "Ptr")
    DllCall("SetWindowLongPtr", "Ptr", hwnd, "Int", -16, "Ptr", (style & ~0xF) | 0xB)
    ; Synchronous full repaint - button never flashes with the default look
    DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
    DllCall("UpdateWindow", "Ptr", hwnd)
}

/**
 * Return the standard a2 color scheme object.
 * @param {(Boolean)} dark - True for the dark palette, false for light.
 * @returns  Object with keys: bg, text, sub, sep, ok, warn, err, btn_bg, acc_fg
 */
a2dlg_colors(dark) {
    if (dark)
        return {
            bg: "202020",
            sub_bg: "181818",
            text: "E8E8E8",
            sub: "888888",
            sep: "444444",
            ok: "36EC95",
            warn: "fff540",
            err: "FF5050",
            btn_bg: "2D2D2D",
            acc_fg: "1A1A1A"
        }
    return {
        bg: "F0F0F0",
        sub_bg: "E8E8E8",
        text: "1A1A1A",
        sub: "666666",
        sep: "C8C8C8",
        ok: "1A9E60",
        warn: "ccb100",
        err: "CC2020",
        btn_bg: "D8D8D8",
        acc_fg: "F8F8F8"
    }
}

/**
 * Apply a dark or light DWM title bar (Windows 10 1809+ / Windows 11).
 * @param {(Integer)} hwnd - Window handle.
 * @param {(Boolean)} dark - True for dark title bar, false for light.
 */
a2dlg_apply_dark_title_bar(hwnd, dark) {
    val := dark ? 1 : 0
    try DllCall("dwmapi\DwmSetWindowAttribute",
        "Ptr", hwnd, "UInt", 20, "Int*", val, "UInt", 4)
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
 * @param {(String)} msg - Message text.
 * @param {(String)} [title] - Window title (default "a2 Information").
 * @param {(Boolean)} [dark] - Force dark/light theme; omit to follow the system setting.
 * @param {(Integer)} [center_on_window] - Optional handle of a window to center the dialog on.
 */
a2dlg_info(msg, title := "a2 Information", dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "💡", "ok", 380, dark, &center_on_window)
    dlg.msg := msg
    dlg.ctrl_c_to_copy_msg()
    dlg.btn_ok()
    _a2dlg_resolve(dlg, center_on_window)
}

/**
 * Show a blocking error popup with an optional selectable detail box and OK button.
 * @param {(String)} msg - Message text.
 * @param {(String)} title - Window title (Default: "a2 Error").
 * @param {(String)} error_detail - Optional selectable detail text shown in a read-only code box.
 * @param {(Boolean)} dark - Force dark/light theme; omit to follow the system setting
 * @param {(Integer)} [center_on_window] - Optional handle of a window to center the dialog on.
 */
a2dlg_error(msg, title := "a2 Error", error_detail := "", dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "❌", "err", 420, dark, &center_on_window)
    dlg.msg := msg

    if (error_detail != "") {
        dlg.code_box(error_detail,,, bottom_line_color:=dlg.c.err)
        dlg.msg .= "`n" error_detail
        dlg.space(6)
        dlg.sep()
    }
    dlg.ctrl_c_to_copy_msg()
    dlg.btn_ok(, , , bg := dlg.c.err, fg := "F8F8F8")
    _a2dlg_resolve(dlg, center_on_window)
}

/**
 * Show blocking question dialog with Yes / No buttons.
 * @example
 *      if a2dlg_yes_no("Delete this item?")
 *          delete_item()
 *
 * @param {(String)} msg - Question text.
 * @param {(String)} [title] - Optional Window title.
 * @param {(Boolean)} [dark] - Optional Force dark/light theme; omit to follow the system setting.
 * @param {(Integer)} [center_on_window] - Optional handle of a window to center the dialog on.
 * @returns  true (Yes) / false (No or closed)
 */
a2dlg_yes_no(msg, title := "a2 Yes/No", dark := -1, center_on_window := 0) {
    t := i18n_domain('general')
    return _a2dlg_confirm(msg, title, t["yes"], t["no"], dark, center_on_window)
}

/**
 * Show blocking confirmation dialog with OK / Cancel buttons.
 * @example
 *      if a2dlg_ok_cancel("Proceed with installation?")
 *          install()
 *
 * @param {(String)} msg - Confirmation text.
 * @param {(String)} [title] - Optional Window title.
 * @param {(Boolean)} [dark] - Optional Force dark/light theme; omit to follow the system setting.
 * @param {(Integer)} [center_on_window] - Optional handle of a window to center the dialog on.
 * @returns {(Boolean)} true (OK) / false (Cancel or closed)
 */
a2dlg_ok_cancel(msg, title := "a2 OK/Cancel", dark := -1, center_on_window := 0) {
    return _a2dlg_confirm(msg, title, "OK",, dark, center_on_window)
}

/**
 * Show a blocking text-input dialog.
 * @example
 *      name := a2dlg_input("Enter your name:", "Name", "World")
 *
 * @param {(String)} msg - Prompt text shown above the input field.
 * @param {(String)} [title] - Window title (Default "a2 Input").
 * @param {(String)} [default_text] - Pre-filled value in the edit field.
 * @param {(Boolean)} [dark] - Force dark/light theme; omit to follow the system setting.
 * @param {(Integer)} [center_on_window] - Optional handle of a window to center the dialog on.
 * @returns {(String)} Entered string, or "" if cancelled.
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

; Helper functions -------------------------------------------------------------

_a2dlg_make(title, msg, glyph, glyph_color, w, dark := -1, &center_on_window := 0) {
    if (center_on_window == 1)
        center_on_window := WinExist('A')
    opts := { w: w, flags: "+AlwaysOnTop -MaximizeBox -MinimizeBox" }
    if dark != -1
        opts.dark := dark
    dlg := A2Dialog(title, opts)
    dlg.space(4)
    row := dlg.glyph_row(glyph, msg,,, {glyph_size: dlg.font_size + 8, glyph_color: dlg.c.%glyph_color%})
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

_a2dlg_confirm(msg, title, ok_label, cancel_label := "", dark := -1, center_on_window := 0) {
    dlg := _a2dlg_make(title, msg, "❓", "warn", 380, dark, &center_on_window)
    dlg.msg := msg
    dlg.ctrl_c_to_copy_msg()
    dlg.btn_ok_cancel(, , ok_label, cancel_label)
    _a2dlg_resolve(dlg, center_on_window)
    return !dlg.cancelled
}

_a2dlg_get_width(ctrl) {
    ctrl.GetPos(,, &ctrl_width)
    return ctrl_width
}

_a2dlg_get_height(ctrl) {
    ctrl.GetPos(,,, &ctrl_height)
    return ctrl_height
}

_a2dlg_get_bottom(ctrl) {
    ctrl.GetPos(,&ctrl_y,, &ctrl_height)
    return ctrl_y + ctrl_height
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
    global _a2dlg_buttons_map, _a2dlg_btn_hover, _a2dlg_pic_map
    _a2dlg_pic_map := Map()
    _a2dlg_buttons_map := Map()
    _a2dlg_btn_hover := 0
    OnMessage(0x2B, _a2dlg_btn_on_draw)        ; WM_DRAWITEM
    OnMessage(0x200, _a2dlg_btn_on_mouse_move)  ; WM_MOUSEMOVE
    OnMessage(0x2A3, _a2dlg_btn_on_mouse_leave) ; WM_MOUSELEAVE
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
_a2dlg_btn_on_draw(wParam, lParam, *) {
    global _a2dlg_buttons_map
    if (NumGet(lParam, 0, "UInt") != 4)     ; CtlType must be ODT_BUTTON = 4
        return
    hwnd := NumGet(lParam, 24, "Ptr")
    if !_a2dlg_buttons_map.Has(hwnd)
        return

    spec := _a2dlg_buttons_map[hwnd]
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
    bg := disabled ? _a2dlg_btn_disabled(spec.bg)
        : (state & 0x1) ? _a2dlg_btn_dim(spec.bg)
            : (_a2dlg_btn_hover = hwnd) ? _a2dlg_btn_lit(spec.bg)
                : spec.bg
    hBrush := DllCall("CreateSolidBrush", "UInt", _a2dlg_btn_gdi(bg), "Ptr")
    DllCall("FillRect", "Ptr", hDC, "Ptr", rc, "Ptr", hBrush)
    DllCall("DeleteObject", "Ptr", hBrush)

    ; Draw label - dim fg when disabled
    hFont := SendMessage(0x31, 0, 0, hwnd)
    old_font := DllCall("SelectObject", "Ptr", hDC, "Ptr", hFont, "Ptr")
    DllCall("SetBkMode", "Ptr", hDC, "Int", 1)
    fg := disabled ? _a2dlg_btn_disabled(spec.fg) : spec.fg
    DllCall("SetTextColor", "Ptr", hDC, "UInt", _a2dlg_btn_gdi(fg))
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
 * @param {(String)} hex  6-digit RRGGBB hex string.
 * @returns  Integer COLORREF value
 */
_a2dlg_btn_gdi(hex) {
    r := Integer("0x" SubStr(hex, 1, 2))
    g := Integer("0x" SubStr(hex, 3, 2))
    b := Integer("0x" SubStr(hex, 5, 2))
    return r | (g << 8) | (b << 16)
}

/**
 * Darken each RGB channel by 30 (clamped to 0) - pressed-state visual feedback.
 * @param {(String)} hex  6-digit RRGGBB hex string.
 * @returns  Darkened 6-digit RRGGBB hex string.
 */
_a2dlg_btn_dim(hex) {
    r := Max(0, Integer("0x" SubStr(hex, 1, 2)) - 30)
    g := Max(0, Integer("0x" SubStr(hex, 3, 2)) - 30)
    b := Max(0, Integer("0x" SubStr(hex, 5, 2)) - 30)
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

/**
 * Lighten each RGB channel by 15 (clamped to 255) - hover-state visual feedback.
 * @param {(String)} hex  6-digit RRGGBB hex string.
 * @returns  Lightened 6-digit RRGGBB hex string.
 */
_a2dlg_btn_lit(hex) {
    r := Min(255, Integer("0x" SubStr(hex, 1, 2)) + 15)
    g := Min(255, Integer("0x" SubStr(hex, 3, 2)) + 15)
    b := Min(255, Integer("0x" SubStr(hex, 5, 2)) + 15)
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

/**
 * Blend each RGB channel 50% toward mid-gray - disabled-state visual feedback.
 * @param {(String)} hex  6-digit RRGGBB hex string.
 * @returns  Muted 6-digit RRGGBB hex string.
 */
_a2dlg_btn_disabled(hex) {
    r := Integer("0x" SubStr(hex, 1, 2))
    g := Integer("0x" SubStr(hex, 3, 2))
    b := Integer("0x" SubStr(hex, 5, 2))
    ; Blend 50% toward mid-gray (128, 128, 128)
    r := (r + 128) // 2
    g := (g + 128) // 2
    b := (b + 128) // 2
    return Format("{:02X}{:02X}{:02X}", r, g, b)
}

/**
 * WM_MOUSEMOVE - fires on the button control; starts leave-tracking if not already active.
 * TRACKMOUSEEVENT layout (x64): cbSize DWORD@0, dwFlags DWORD@4, hwndTrack Ptr@8, dwHoverTime DWORD@16
 */
_a2dlg_btn_on_mouse_move(wParam, lParam, msg, hwnd) {
    global _a2dlg_buttons_map, _a2dlg_btn_hover, _a2dlg_pic_map
    if _a2dlg_pic_map.Has(hwnd) && (_a2dlg_btn_hover != hwnd) {
        _a2dlg_btn_hover := hwnd
        pic := _a2dlg_pic_map[hwnd]
        pic.Value := pic.icon_hover
        _a2dlg_track_mouse_leave(hwnd)
        return
    }
    if !_a2dlg_buttons_map.Has(hwnd) || (_a2dlg_btn_hover = hwnd)
        return
    _a2dlg_btn_hover := hwnd
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
_a2dlg_btn_on_mouse_leave(wParam, lParam, msg, hwnd) {
    global _a2dlg_buttons_map, _a2dlg_btn_hover, _a2dlg_pic_map
    if _a2dlg_btn_hover = hwnd
        _a2dlg_btn_hover := 0
    if _a2dlg_pic_map.Has(hwnd) {
        pic := _a2dlg_pic_map[hwnd]
        pic.Value := pic.checked ? pic.icon_on : pic.icon_off
        return
    }
    if _a2dlg_buttons_map.Has(hwnd) {
        DllCall("InvalidateRect", "Ptr", hwnd, "Ptr", 0, "Int", 1)
        DllCall("UpdateWindow", "Ptr", hwnd)
    }
}

_a2dlg_track_mouse_leave(hwnd) {
    tme := Buffer(24, 0)
    NumPut("UInt", 24,  tme, 0)
    NumPut("UInt", 0x2, tme, 4)   ; TME_LEAVE
    NumPut("Ptr", hwnd, tme, 8)
    DllCall("TrackMouseEvent", "Ptr", tme)
}