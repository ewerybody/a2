if (a2_startup_tool_tips == "true")
    tt(a2_title, 0.5)

this_call := a2dev_get_py() " a2app.py"
ui_path = %A_ScriptDir%\..\ui\
Run, %this_call%, %ui_path%

sleep 500


Return ; -----------------------------------------------------------------------------
#include a2_config.ahk
#include a2dev_find_py.ahk
