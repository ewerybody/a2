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
time_check := dlg.checkbox("Timeout (Seconds):",1,,, check_toggled)
time_field := dlg.add("Edit", "w50 Number -E0x200 Background" dlg.c.sub_bg, next_to := time_check.label)
time_field.OnEvent("Change", _time_field_change)
time_up_down := dlg.add("UpDown", "Range1-10", next_to := time_field, 2)
time_slider := dlg.add("Slider", "Range1-10 AltSubmit", next_to := time_up_down, 2, max_width := true)
time_slider.OnEvent("Change", _time_slider_change)
using_timeout_msg := 'Using timeout ^'
sub_text := dlg.text(using_timeout_msg)

dlg.btn_row_right([{label: "Remove a2tip", func: remove_tip}, {label: "Close", func: (*) => dlg.destroy()}], )
dlg.esc_to_close()
dlg.exit_on_close()
dlg.show()

show_tip(*){
    if (time_check.checked) {
        a2tip(text_field.Text, time_field.Value)
        return
    }
    a2tip(text_field.Text)
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

check_toggled(value) {
    time_up_down.Enabled := value
    time_slider.Enabled := value
    update_subtext()
}

update_subtext(*) {
    sub_text.Text := time_check.checked ? using_timeout_msg : "Using timeout estimation (" StrLen(text_field.text) / 20 * 1000 "ms)"
}