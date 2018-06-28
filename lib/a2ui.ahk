a2_ui_call := _init_get_var("a2_ui_call")
a2_startup_tool_tips := _init_get_var("a2_startup_tool_tips")

StringLower, a2_startup_tool_tips, a2_startup_tool_tips
if (a2_startup_tool_tips == "true")
    tt("a2ui...", 0.5)

StringLower, a2_ui_call, a2_ui_call
if (SubStr(a2_ui_call, -3) == ".exe")
	this_call := a2_ui_call
else
	this_call := a2dev_get_py() " " a2_ui_call

MsgBox this_call: %this_call%
    
ui_path = %A_ScriptDir%\..\ui\
Run, %this_call%, %ui_path%

sleep 500


Return ; -----------------------------------------------------------------------------
#include a2init_check.ahk
#include *i a2dev_find_py.ahk
