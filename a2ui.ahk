#include a2_settings.ahk
Gosub, a2ui

return
#include lib\tt.ahk

a2ui:
    global a2_python
    if a2_startup_tool_tips
        tt("a2ui...", 0.5)
    Run, %a2_python% a2app.py, %A_ScriptDir%\ui\
    sleep 500
return
