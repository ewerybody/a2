if (a2_startup_tool_tips == "true")
    tt(a2_title, 0.5)

ui_path = %A_ScriptDir%\..\ui\
Run, a2app.exe, %ui_path%

sleep 500


Return ; -----------------------------------------------------------------------------
#include a2_config.ahk
