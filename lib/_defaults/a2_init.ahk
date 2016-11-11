#include settings\variables.ahk
#include settings\libs.ahk
#include settings\includes.ahk
#include settings\hotkeys.ahk
#include settings\init.ahk

init_func := "a2_init_calls"
if IsFunc(init_func) %init_func%()
