; Demo + test for a2dlg.ahk.
;
; What to test:
;   - Colors render correctly for each button variant
;   - Pressed state (click + hold) visibly darkens the button
;   - Tab key moves focus; focused button shows a dotted focus ring
;   - Enter fires the Default button (✓ Accent); Space fires the focused button
;   - "Toggle Dark / Light" rebuilds the dialog in the other theme
;   - Clicking any color button updates the status line at the bottom
;
#Requires AutoHotkey v2.0
#NoTrayIcon
#Include ..\a2dlg.ahk

a2dlg_demo()

; ================================================================
;  Demo window
; ================================================================
a2dlg_demo(forced_dark := unset) {
    icon_path := A_ScriptDir "\..\..\..\..\ui\res\a2.ico"

    opts := {w: 468, pad: 16}
    if IsSet(forced_dark)
        opts.dark := forced_dark
    d := A2Dialog("A2 Dialog Demo", opts)
    c := d.c

    d.header("Welcome to the A2 Dialog Demo", icon_path)
    d.sep()

    ; ---- Button grid ----
    ; Row 1 — three semantic variants
    row1 := d.btn_row([
        {label: "✓  Accent",    bg: c.ok,     fg: c.acc_fg, opts: "Default"},
        {label: "Neutral",       bg: c.btn_bg, fg: c.text},
        {label: "⚠  Warning",   bg: c.warn,   fg: "1A1A1A"}
    ], 30, 8, 136)

    ; Row 2 — danger + a custom color swatch
    row2 := d.btn_row([
        {label: "✗  Danger",     bg: c.err,   fg: "F8F8F8"},
        {label: "Custom (teal)", bg: "117A8B", fg: "E8F8FF"}
    ], 30, 8, 136)
    d.space(10)

    ; ---- Status line ----
    status := d.text("Click any button above…")
    theme_str := "Theme: " (IsSet(forced_dark) ? "Set to" : "System default") ": " (d.dark ? "Dark" : "Light")
    theme := d.text(theme_str)
    d.sep()

    ; ---- Popup dialog comparison (2-column) ----
    d.sep()
    d.gui.SetFont("s" (d._fsz + 1) " w700 c" c.text, d._face)
    d.gui.AddText("x" d._pad " y" d._y " w" (d._w - d._pad * 2), "Popup dialogs")
    d._y += 26
    d.gui.SetFont("s" (d._fsz - 1) " w400 c" c.sub, d._face)
    col_w := (d._w - d._pad * 2 - 8) // 2
    d.gui.AddText("x" d._pad " y" d._y " w" col_w, "a2dlg version")
    d.gui.AddText("x" (d._pad + col_w + 8) " y" d._y " w" col_w, "AHK built-in")
    d._y += 18

    popup_rows := [
        ["ℹ  Info",        "a2dlg_info",     "MsgBox (info)"],
        ["✗  Error",      "a2dlg_error",    "MsgBox (error)"],
        ["?  Yes / No",   "a2dlg_yes_no",   "MsgBox (yes no)"],
        ["?  OK / Cancel","a2dlg_ok_cancel","MsgBox (ok cancel)"],
        ["✎  Input",     "a2dlg_input",    "InputBox"],
    ]
    popup_buttons_a2  := []
    popup_buttons_ahk := []
    for row in popup_rows {
        bh := 26
        ; a2dlg column
        b1 := d.gui.AddButton("x" d._pad " y" d._y " w" col_w " h" bh, row[1] "  →  " row[2])
        a2dlg_make_button(b1, c.btn_bg, c.text)
        d._btn_hwnds.Push(b1.Hwnd)
        popup_buttons_a2.Push({btn: b1, kind: row[2]})
        ; AHK column
        b2 := d.gui.AddButton("x" (d._pad + col_w + 8) " y" d._y " w" col_w " h" bh, row[3])
        a2dlg_make_button(b2, c.btn_bg, c.text)
        d._btn_hwnds.Push(b2.Hwnd)
        popup_buttons_ahk.Push({btn: b2, kind: row[3]})
        d._y += bh + 6
    }
    d._y += 2

    ; ---- Footer: toggle + close ----
    d.sep()
    footer := d.btn_row_right([
        {label: d.dark ? "Switch to Light Mode" : "Switch to Dark Mode", bg: c.btn_bg, fg: c.text},
        {label: "Close", bg: c.btn_bg, fg: c.text}
    ], 160)

    d.show()
    d.set_icon(icon_path)
    d.esc_to_close()

    ; ---- Click events — button grid ----
    row1[1].OnEvent("Click", (*) => (status.Text := "Clicked: Accent (Default button / Enter key)"))
    row1[2].OnEvent("Click", (*) => (status.Text := "Clicked: Neutral"))
    row1[3].OnEvent("Click", (*) => (status.Text := "Clicked: Warning"))
    row2[1].OnEvent("Click", (*) => (status.Text := "Clicked: Danger"))
    row2[2].OnEvent("Click", (*) => (status.Text := "Clicked: Custom teal"))

    ; ---- Click events — popup comparison ----
    ; Store kind on the control itself so each handler reads its own value,
    ; not the shared loop variable (which would always be the last value).
    for item in popup_buttons_a2 {
        item.btn.kind := item.kind
        item.btn.OnEvent("Click", (ctrl, *) => _demo_popup_a2(ctrl.kind, status, d.dark))
    }
    for item in popup_buttons_ahk {
        item.btn.kind := item.kind
        item.btn.OnEvent("Click", (ctrl, *) => _demo_popup_ahk(ctrl.kind, status))
    }

    ; Defer destroy+recreate so AHK fully exits the current event handler first
    footer[1].OnEvent("Click", (*) => SetTimer(() => (d.destroy(), a2dlg_demo(!d.dark)), -1))
    footer[2].OnEvent("Click", (*) => ExitApp())
    d.on_close((*) => ExitApp())
}

; ---- Popup demo handlers ----
_demo_popup_a2(kind, status, dark) {
    if (kind = "a2dlg_info") {
        a2dlg_info("This is an informational message.", "a2 Info", dark)
        status.Text := "a2dlg_info — dismissed"
    } else if (kind = "a2dlg_error") {
        a2dlg_error("Something went wrong.", "a2 Error", "Error detail line 1`nError detail line 2`nLine 3", dark)
        status.Text := "a2dlg_error — dismissed"
    } else if (kind = "a2dlg_yes_no") {
        result := a2dlg_yes_no("Do you want to continue?", "a2 Yes/No", dark)
        status.Text := "a2dlg_yes_no → " (result ? "Yes" : "No")
    } else if (kind = "a2dlg_ok_cancel") {
        result := a2dlg_ok_cancel("Proceed with the operation?", "a2 OK/Cancel", dark)
        status.Text := "a2dlg_ok_cancel → " (result ? "OK" : "Cancel")
    } else if (kind = "a2dlg_input") {
        result := a2dlg_input("Enter your name:", "a2 Input", "World", dark)
        status.Text := (result = "") ? "a2dlg_input → (cancelled)" : "a2dlg_input → `"" result "`""
    }
}

_demo_popup_ahk(kind, status) {
    if (kind = "MsgBox (info)") {
        MsgBox("This is an informational message.", "AHK Info", "OK Iconi")
        status.Text := "MsgBox info — dismissed"
    } else if (kind = "MsgBox (error)") {
        MsgBox("Something went wrong.", "AHK Error", "OK Iconx")
        status.Text := "MsgBox error — dismissed"
    } else if (kind = "MsgBox (yes no)") {
        result := MsgBox("Do you want to continue?", "AHK Yes/No", "YesNo Icon?")
        status.Text := "MsgBox YesNo → " result
    } else if (kind = "MsgBox (ok cancel)") {
        result := MsgBox("Proceed with the operation?", "AHK OK/Cancel", "OKCancel Icon?")
        status.Text := "MsgBox OKCancel → " result
    } else if (kind = "InputBox") {
        result := InputBox("Enter your name:", "AHK InputBox", , "World")
        status.Text := (result.Result = "Cancel") ? "InputBox → (cancelled)" : "InputBox → `"" result.Value "`""
    }
}
