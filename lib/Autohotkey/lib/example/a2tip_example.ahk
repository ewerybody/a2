; Example Tool to test and showcase the `a2tip` capabilities.
#SingleInstance Force
#NoTrayIcon
#Include <a2tip>

a2tip("hallo")

A2TipUI := Gui("+DPIScale +Resize +MinSize500x180")
A2TipUI.OnEvent("Escape", A2TipUI.Destroy)
show_btn := A2TipUI.AddButton("xm Section", "Show a2tip")
show_btn.OnEvent("Click", show_tip)
text_field := A2TipUI.AddEdit("ys w400 Multi", "Hello,`nNew World!")

A2TipUI.AddText("xm Section", "Timeout (Seconds):")
time_field := A2TipUI.AddEdit("ys w50 Section Number")
time_field.OnEvent("Change", _time_field_change)
time_updown := A2TipUI.AddUpDown("Range1-10", 2)
time_slider := A2TipUI.AddSlider("ys w320 Range1-10 AltSubmit", 2)
time_slider.OnEvent("Change", _time_slider_change)

remove_btn := A2TipUI.AddButton("xm", "Remove a2tip")
remove_btn.OnEvent("Click", remove_tip)
A2TipUI.Show()

show_tip(*){
    a2tip(text_field.Text, time_field.Value)
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