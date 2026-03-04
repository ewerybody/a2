; audio_example.ahk
; Interactive example / manual test for lib/audio.ahk
; Shows all active output devices, marks the current default,
; and lets you switch with a button click.
;
; Run standalone from the a2 repo root:
;   AutoHotkey.exe extras\examples\audio_example.ahk

#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon

#Include <audio>
#Include <a2dlg>

audio_example()

audio_example() {
    dlg := A2Dialog("Audio Output Devices", {w: 440})

    devices    := audio_get_output_devices()
    current_id := audio_get_default_output()

    dlg.header("🔊 Audio Output Devices")
    dlg.text("There are " devices.Length " active render endpoints on this machine:")
    dlg.sep()

    if !devices.Length {
        dlg.row("⚠", dlg.c.warn, "No active output devices found!")
    } else {
        ; One row + one button per device — all created upfront
        rows := []
        for dev in devices {
            is_current := dev.id = current_id
            row_ref := dlg.glyph_row(is_current ? "✔" : "◦", dev.name,,, is_current)
            btns := dlg.btn_row([{label: "Switch here", bg: dlg.c.btn_bg, fg: dlg.c.text}], 24, 0, 110)
            rows.Push({id: dev.id, name: dev.name, row: row_ref, btn: btns[1]})
            if is_current {
                dlg.set_color(dlg.c.ok, row_ref)
                btns[1].Enabled := false
            }
        }
        status := dlg.text("Current: " _audio_example_name(rows, current_id))
        ; Wire switch buttons
        for item in rows
            item.btn.OnEvent("Click", _do_switch.Bind(item.id, rows, dlg, status))
    }

    dlg.space(4)
    dlg.sep()
    dlg.btn_close()
    dlg.exit_on_close()
    dlg.esc_to_close()
    dlg.show()
}

_do_switch(new_id, rows, dlg, status, *) {
    audio_set_default_output(new_id)
    for item in rows {
        is_current := item.id = new_id
        item.row.glyph.Text := is_current ? "✔" : "◦"
        if !is_current
            dlg.set_active(item.row)
        else
            dlg.set_color(dlg.c.ok, item.row)
        item.row.Enabled := !is_current
        item.btn.Enabled := !is_current
    }
    status.Text := "Current: " _audio_example_name(rows, new_id)
}

_audio_example_name(rows, id) {
    for item in rows {
        if item.id = id
            return item.name
    }
    return id
}