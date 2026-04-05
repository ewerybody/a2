; Demo + test for a2dlg.ahk.
;
; What to test:
;   - Colors render correctly for each button variant
;   - Pressed state (click + hold) visibly darkens the button
;   - Tab key moves focus; focused button shows a dotted focus ring
;   - Enter fires the Default button (✔️ Accent); Space fires the focused button
;   - "Toggle Dark / Light" rebuilds the dialog in the other theme
;   - Clicking any color button updates the status line at the bottom
;
#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

#Include <path>
#Include ../../../a2_globals.ahk
#Include <a2dlg>
#Include <i18n>
#Include <window>

a2dlg_demo()

a2dlg_demo(forced_dark := unset) {
    global _ := i18n_locale(A_LineFile)

    opts := { w: 468, pad: 16 }
    if IsSet(forced_dark)
        opts.dark := forced_dark
    dlg := A2Dialog("A2 Dialog Demo", opts)
    dlg.header(_["welcome"], dlg.a2_icon)
    dlg.sep()

    ; Button grid
    ; Row 1 — three semantic variants
    row1 := dlg.btn_row([
        { label: "✔️  Accent", bg: dlg.c.ok, fg: dlg.c.acc_fg, opts: "Default"
        , func: (*) => (status.Text := "Clicked: Accent (Default button / Enter key)") },
        { label: "Neutral", func: (*) => (status.Text := "Clicked: Neutral") },
        { label: "⚠️  Warning", bg: dlg.c.warn, fg: "1A1A1A", func: (*) => (status.Text := "Clicked: Warning")}],
        30, 8, 136)
    ; Row 2 — danger + a custom color swatch
    row2 := dlg.btn_row([
        { label: "❌  Danger", bg: dlg.c.err, fg: "F8F8F8", func: (*) => (status.Text := "Clicked: Danger") },
        { label: "Custom (teal)", bg: "117A8B", fg: "E8F8FF", func: (*) => (status.Text := "Clicked: Custom teal") }],
        30, 8, 136)
    dlg.space(10)

    ; Status line
    status := dlg.text(_["click"])
    theme_str := "Theme: " (IsSet(forced_dark) ? "Set to" : "System default") ": " (dlg.dark ? "Dark" : "Light")
    theme := dlg.text(theme_str)
    dlg.sep()

    ; Popup dialog comparison (2-column)
    dlg.heading("Popup dialogs")
    dlg.gui.SetFont("s" (dlg.font_size - 1) " w400 c" dlg.c.sub, dlg.font_face)
    col_w := (dlg.width - dlg.pad * 2 - 8) // 2
    dlg.gui.AddText("x" dlg.pad " y" dlg.height " w" col_w, "a2dlg version")
    dlg.gui.AddText("x" (dlg.pad + col_w + 8) " y" dlg.height " w" col_w, "AHK built-in")
    dlg.space(18)

    popup_rows := [
        ["a2dlg_info", "MsgBox (info)"],
        ["a2dlg_error", "MsgBox (error)"],
        ["a2dlg_yes_no", "MsgBox (yes no)"],
        ["a2dlg_ok_cancel", "MsgBox (ok cancel)"],
        ["a2dlg_input", "InputBox"],
    ]
    popup_buttons_a2 := []
    popup_buttons_ahk := []
    for row in popup_rows {
        btns := dlg.btn_row([{ label: row[1]}, { label: row[2] }], 26, 8)
        popup_buttons_a2.Push({ btn: btns[1], kind: row[1] })
        popup_buttons_ahk.Push({ btn: btns[2], kind: row[2] })
    }

    dlg.sep()
    footer := dlg.btn_row_right([
        { label: dlg.dark ? _["light_mode"] : _["dark_mode"]
        , func: (*) => SetTimer(() => (dlg.destroy(), a2dlg_demo(!dlg.dark)), -1)},
        { label: "Close", w: 100, func: (*) => ExitApp() }
    ])

    ; Store kind on the control itself so each handler reads its own value,
    ; not the shared loop variable (which would always be the last value).
    for item in popup_buttons_a2 {
        item.btn.kind := item.kind
        item.btn.OnEvent("Click", (ctrl, *) => _demo_popup_a2(ctrl.kind, status, dlg.dark))
    }
    for item in popup_buttons_ahk {
        item.btn.kind := item.kind
        item.btn.OnEvent("Click", (ctrl, *) => _demo_popup_ahk(ctrl.kind, status))
    }

    ; To enable light-dark-mode switching we move around our built-ins `exit_on_close` and `esc_to_close`:
    ; Defer destroy+recreate so AHK fully exits the current event handler first
    dlg.on_close((*) => ExitApp())
    dlg.on_escape((*) => ExitApp())

    dlg.show()
}

; Popup a2dlg demo handlers.
_demo_popup_a2(kind, status, dark) {
    if (kind = "a2dlg_info") {
        a2dlg_info(_["info"], , dark)
        status.Text := "a2dlg_info — dismissed"
    } else if (kind = "a2dlg_error") {
        a2dlg_error(_["error"], , "Error detail line 1`nError detail line 2`nLine 3", dark)
        status.Text := "a2dlg_error — dismissed"
    } else if (kind = "a2dlg_yes_no") {
        result := a2dlg_yes_no(_["continue"], , dark)
        status.Text := "a2dlg_yes_no => " (result ? "Yes" : "No")
    } else if (kind = "a2dlg_ok_cancel") {
        result := a2dlg_ok_cancel(_["proceed"], , dark)
        status.Text := "a2dlg_ok_cancel => " (result ? "OK" : "Cancel")
    } else if (kind = "a2dlg_input") {
        result := a2dlg_input(Format(_["name_please"], _["your_name"]), "a2 Input", "Hello, World!", dark)
        if result = _["your_name"]
            a2dlg_info(_["very_funny"], , dark)
        status.Text := (result = "") ? "a2dlg_input => (cancelled)" : "a2dlg_input => `"" result "`""
    }
}

; Popup built-in AHK demo handlers.
_demo_popup_ahk(kind, status) {
    if (kind = "MsgBox (info)") {
        MsgBox(_["info"], "AHK Info", "OK Iconi")
        status.Text := "MsgBox info — dismissed"
    } else if (kind = "MsgBox (error)") {
        MsgBox(_["error"], "AHK Error", "OK Iconx")
        status.Text := "MsgBox error — dismissed"
    } else if (kind = "MsgBox (yes no)") {
        result := MsgBox(_["continue"], "AHK Yes/No", "YesNo Icon?")
        status.Text := "MsgBox YesNo => " result
    } else if (kind = "MsgBox (ok cancel)") {
        result := MsgBox(_["proceed"], "AHK OK/Cancel", "OKCancel Icon?")
        status.Text := "MsgBox OKCancel => " result
    } else if (kind = "InputBox") {
        result := InputBox(Format(_["name_please"], _["your_name"]), "AHK InputBox", , "World")
        if result.Value = _["your_name"]
            MsgBox(_["very_funny"])
        status.Text := (result.Result = "Cancel") ? "InputBox => (cancelled)" : "InputBox => `"" result.Value "`""
    }
}
