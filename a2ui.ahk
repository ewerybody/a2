#include a2_settings.ahk
IfExist, %a2_python%
    Run, %a2_python% a2app.py, %A_ScriptDir%\ui
