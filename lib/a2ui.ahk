a2_ui_call := _init_get_var("a2_ui_call")

a2_startup_tool_tips := _init_get_var("a2_startup_tool_tips")

StringLower, a2_startup_tool_tips, a2_startup_tool_tips
if (a2_startup_tool_tips == "true")
    tt("a2ui...", 0.5)

ui_path = %A_ScriptDir%\..\ui\
Run, %a2_ui_call%, %ui_path%
sleep 500

Return ; -----------------------------------------------------------------------------
#include a2init_check.ahk
#include tt.ahk
