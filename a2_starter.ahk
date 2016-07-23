settings_created := _init_check_settings()
a2_ahk := _init_get_var("a2_ahk")

Run, %a2_ahk% a2.ahk

if settings_created
{
    MsgBox, 65, a2 Settings Created!, Default settings have just been created, do you want to open up the a2 User Interface to make further changes?
    IfMsgBox, Ok
        Run, a2ui.ahk        
}

Return
#include lib\_init_check.ahk
