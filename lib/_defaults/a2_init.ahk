#include settings\variables.ahk
initFunc := "a2_init_calls"
if IsFunc(initFunc)
    %initFunc%()
#include settings\libs.ahk
#include settings\includes.ahk
#include settings\hotkeys.ahk
#include settings\init.ahk
