; a2dlg_builder.ahk
; Live dialog builder — add features from a palette, see the result instantly.
; The preview is a real A2Dialog script running in a separate process.
;
; Run standalone from the a2 lib/Autohotkey root:
;   AutoHotkey.exe lib\example\a2dlg_builder.ahk

#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

#Include <a2dlg>

A2dlgBuilder()

class A2dlgBuilder {
    static FEATURES := [
        {label: "header",        code: 'd.header("My Dialog")'},
        {label: "sep",           code: "d.sep()"},
        {label: "glyph_row",     code: 'd.glyph_row("✔", "Everything is fine", d.c.ok)'},
        {label: "text",          code: 'd.text("Some caption or status line.")'},
        {label: "space",         code: "d.space(12)"},
        {label: "heading",       code: 'd.heading("Section")'},
        {label: "edit_field",    code: "d.edit_field()"},
        {label: "code_box",      code: 'd.code_box("error detail here")'},
        {label: "btn_ok",        code: "d.btn_ok()"},
        {label: "btn_close",     code: "d.btn_close()"},
        {label: "btn_ok_cancel", code: "d.btn_ok_cancel()"},
    ]

    stack        := []
    preview_pid  := 0
    preview_tmp  := A_Temp "\a2dlg_builder_preview.ahk"
    dlg          := ""
    stack_ctrl   := ""
    code_ctrl    := ""

    __New() {
        d := A2Dialog("a2dlg Builder", {w: 520})
        this.dlg := d
        c := d.c

        d.header("🧱 a2dlg Builder")
        d.text("Click features to add them to your dialog.")
        d.sep()

        d.heading("Add feature")
        d.space(4)
            for i, feat in A2dlgBuilder.FEATURES {
            btns := d.btn_row([{label: "+ " feat.label}], 26, 0, 160)
                btns[1].OnEvent("Click", this._on_add.Bind(this, i))
            d.space(2)
        }

        d.space(6)
        d.sep()

        d.heading("Current stack")
        d.space(4)
            this.stack_ctrl := d.text("(empty)", c.sub)

        d.space(6)
        d.sep()

        d.heading("Generated code")
        d.space(4)
        this.code_ctrl := d.code_box("", 120)
        d.space(6)
        d.sep()

        footer := d.btn_row_right([
            {label: "↩ Undo",   w: 80},
            {label: "🗑 Clear",  w: 80},
            {label: "Close",     w: 80}
        ])
            footer[1].OnEvent("Click", (*) => this._undo())
            footer[2].OnEvent("Click", (*) => this._clear())
        footer[3].OnEvent("Click", (*) => ExitApp())
        d.on_close((*) => ExitApp())
        d.esc_to_close()
        d.show()
    }

    _on_add(feat_idx, ctrl, *) {
        this.stack.Push(feat_idx)
        this._refresh()
    }

    _undo() {
        if this.stack.Length
            this.stack.RemoveAt(this.stack.Length)
        this._refresh()
    }

    _clear() {
        this.stack := []
        this._refresh()
    }

    _refresh() {
        feats := A2dlgBuilder.FEATURES

        lines := []
        for feat_idx in this.stack
            lines.Push("    " feats[feat_idx].code)
        code_str := lines.Length ? string_join(lines, "`n") : ""

        ; Update code display
        this.code_ctrl.Value := code_str

        ; Update stack label
        if this.stack.Length {
            names := []
            for feat_idx in this.stack
                names.Push(feats[feat_idx].label)
            this.stack_ctrl.Text := string_join(names, "  →  ")
        } else {
            this.stack_ctrl.Text := "(empty)"
        }

        ; Kill previous preview
        if this.preview_pid {
            try ProcessClose(this.preview_pid)
            this.preview_pid := 0
        }

        ; Don't launch an empty preview
        if !this.stack.Length
            return

        ; Position preview to the right of the builder
        WinGetPos(&bx, &by, &bw, , "ahk_id " this.dlg.hwnd)
        preview_x := bx + bw + 12
        preview_y := by

        ; Write and launch
        script := this._build_script(code_str, preview_x, preview_y)
        try FileDelete(this.preview_tmp)
        FileAppend(script, this.preview_tmp, "UTF-8")
        Run(A_AhkPath " " this.preview_tmp, , , &pid)
        this.preview_pid := pid
    }

    _build_script(code_lines, x, y) {
        return (
            "#Requires AutoHotkey v2.0`n"
            "#SingleInstance Force`n"
            "#NoTrayIcon`n"
            "`n"
            "#Include <a2dlg>`n"
            "`n"
                "d := A2Dialog(`"Preview`", {w: 380, x: " x ", y: " y "})`n"
            code_lines "`n"
            "d.esc_to_close()`n"
            "d.show()`n"
            "WinWaitClose(`"ahk_id `" d.hwnd)`n"
        )
    }
}
