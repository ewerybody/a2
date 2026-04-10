; a2dlg_builder.ahk
; Live dialog builder — add features from a palette, see the result instantly.
; The preview is a real A2Dialog script running in a separate process.
;
; Run standalone from the a2 lib/Autohotkey root:
;   AutoHotkey.exe lib\example\a2dlg_builder.ahk

#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

#Include ../../../a2icon.ahk
#Include <a2dlg>
#Include <path>

A2dlgBuilder()

class A2dlgBuilder {
    static FEATURES := [
        {label: "header",        code: 'dlg.header("My Dialog")'},
        {label: "sep",           code: "dlg.sep()"},
        {label: "glyph_row",     code: 'dlg.glyph_row("✔", "Everything is fine", dlg.c.ok)'},
        {label: "text",          code: 'dlg.text("Some caption or status line.")'},
        {label: "space",         code: "dlg.space(12)"},
        {label: "heading",       code: 'dlg.heading("Section")'},
        {label: "edit_field",    code: "dlg.edit_field()"},
        {label: "code_box",      code: 'dlg.code_box("error detail here")'},
        {label: "btn",           code: "dlg.btn('Hello')"},
        {label: "btn_ok",        code: "dlg.btn_ok()"},
        {label: "btn_close",     code: "dlg.btn_close()"},
        {label: "btn_ok_cancel", code: "dlg.btn_ok_cancel()"},
    ]

    stack        := []
    preview_pid  := 0
    preview_tmp  := A_Temp "\a2dlg_builder_preview.ahk"
    dlg          := ""
    stack_ctrl   := ""
    code_ctrl    := ""
    lib_path     := path_dirname(A_ScriptDir, 3)

    __New() {
        dlg := A2Dialog("a2dlg Builder", {w: 520})
        this.dlg := dlg
        c := dlg.c

        dlg.header("🧱 a2dlg Builder")
        dlg.text("Click features to add them to your dialog.")
        dlg.sep()

        dlg.heading("Add feature")
        dlg.space(4)
            for i, feat in A2dlgBuilder.FEATURES {
            buttons := dlg.btn_row([{label: "+ " feat.label}], 160, 26, 0)
            buttons[1].OnEvent("Click", this._on_add.Bind(this, i))
            dlg.space(2)
        }

        dlg.space(6)
        dlg.sep()

        dlg.heading("Current stack")
        dlg.space(4)
            this.stack_ctrl := dlg.text("(empty)", c.sub)

        dlg.space(6)
        dlg.sep()

        dlg.heading("Generated code")
        dlg.space(4)
        this.code_ctrl := dlg.code_box("", 120)
        dlg.space(6)
        dlg.sep()

        footer := dlg.btn_row_right([
            {label: "↩ Undo", w: 80},
            {label: "🗑 Clear", w: 80},
            {label: "Close", w: 80}
        ])
            footer[1].OnEvent("Click", (*) => this._undo())
            footer[2].OnEvent("Click", (*) => this._clear())
        footer[3].OnEvent("Click", (*) => ExitApp())
        dlg.on_close((*) => ExitApp())
        dlg.esc_to_close()
        dlg.show()
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
            "#Include " this.lib_path "\a2icon.ahk`n"
            "#Include <a2dlg>`n"
            "`n"
                "dlg := A2Dialog(`"Preview`", {w: 380, x: " x ", y: " y "})`n"
            code_lines "`n"
            "dlg.esc_to_close()`n"
            "dlg.show()`n"
            "WinWaitClose(`"ahk_id `" dlg.hwnd)`n"
        )
    }
}
