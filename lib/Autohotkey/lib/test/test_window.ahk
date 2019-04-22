#Include  %A_ScriptDir%\..\ahk_functions.ahk
#Include  %A_ScriptDir%\..\window.ahk
#Include  %A_ScriptDir%\..\screen.ahk

msgbox window_toggle_maximize ...
window_toggle_maximize()
msgbox window_toggle_maximize ...
window_toggle_maximize()

msgbox window_toggle_maximize_width ...
window_toggle_maximize_width()
msgbox window_toggle_maximize_width ...
window_toggle_maximize_width()

msgbox window_toggle_maximize_height ...
window_toggle_maximize_height()
msgbox window_toggle_maximize_height ...
window_toggle_maximize_height()

x := window_is_resizable()
if x
    msgbox window_is_resizable! : %x%
else
    msgbox window_is NOT resizable! : %x%

