a2_python := _init_get_var("a2_python")
a2_startup_tool_tips := _init_get_var("a2_startup_tool_tips")

if a2_startup_tool_tips
    tt("a2ui...", 0.5)
Run, %a2_python% a2app.py, %A_ScriptDir%\ui\
sleep 500

Return
#include lib\_init_check.ahk
#include lib\tt.ahk
