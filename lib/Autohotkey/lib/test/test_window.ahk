#Include  %A_ScriptDir%\..\ahk_functions.ahk
#Include  %A_ScriptDir%\..\window.ahk
#Include  %A_ScriptDir%\..\screen.ahk
window_toggle_maximize()


x := window_is_resizable()
if x
    msgbox window_is_resizable! : %x%
else
    msgbox window_is NOT resizable! : %x%

