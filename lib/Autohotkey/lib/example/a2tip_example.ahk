; Example Tool to test and showcase the `a2tip` capabilities.
#SingleInstance Force
#NoTrayIcon

#Include <a2tip>
#Include <a2dlg>

a2tip("hallo")

dlg := A2Dialog("A2 Dialog Demo")
btn := dlg.btn("Show a2tip", show_tip,, 50)
text_field := dlg.edit_field("Hello,`nNew World!", rows := 3, next_to := btn)
text_field.OnEvent("Change", update_subtext)
time_check := dlg.checkbox("Timeout (Seconds):",1,, time_toggled)
time_field := dlg.add("Edit", "w50 Number -E0x200 Background" dlg.c.sub_bg, next_to := time_check.label)
time_field.OnEvent("Change", _time_field_change)
time_up_down := dlg.add("UpDown", "Range1-10",, 2)
time_slider := dlg.add("Slider", "Range1-10 AltSubmit", next_to := time_up_down, 2, max_width := true)
time_slider.OnEvent("Change", _time_slider_change)
using_timeout_msg := 'Using timeout ^'
sub_text := dlg.text(using_timeout_msg)
font_check := dlg.checkbox("Font Size:",0)
font_size := dlg.add("Edit", "w50 Number -E0x200 Background" dlg.c.sub_bg, next_to := font_check.label)
font_up_down := dlg.add("UpDown", "Range5-40",, 2)
font_size.Value := 10
font_label := dlg.btn("Font Face:",pick_font ,,,,,, next_to:=font_up_down)
font_field := dlg.edit_field("Comic Sans MS",, next_to := font_label, read_only := true)

; font_field := dlg.edit_field("Comic Sans",, next_to := font_check)
; font_field.OnEvent("Change", _time_field_change)

dlg.btn_row_right([{label: "Remove a2tip", func: remove_tip}, {label: "Close", func: (*) => dlg.destroy()}], )
dlg.esc_to_close()
dlg.exit_on_close()
dlg.show()

show_tip(*){
    font := font_check.checked ? "s" font_size.Value ", " font_field.Value : ""
    if (time_check.checked) {
        a2tip(text_field.Text "`n" font, time_field.Value, font)
        return
    }
    a2tip(text_field.Text,, font)
}

remove_tip(*){
    a2tip()
}

_time_slider_change(*) {
    time_field.Value := time_slider.Value
}

_time_field_change(*) {
    time_slider.Value := time_field.Value
}

time_toggled(value) {
    time_up_down.Enabled := value
    time_slider.Enabled := value
    update_subtext()
}

update_subtext(*) {
    sub_text.Text := time_check.checked ? using_timeout_msg : "Using timeout estimation (" StrLen(text_field.text) / 20 * 1000 "ms)"
}

pick_font(*) {
    font_obj := font_pick(dlg.hwnd, current := {face: font_field.Value, size: font_size.Value})
    font_size.Value := font_obj.size
    font_field.Value := font_obj.face
}