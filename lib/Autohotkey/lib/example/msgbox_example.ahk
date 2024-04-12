#include ..\msgbox.ahk

msgbox_info("Example info message box! 🙂", "a2 lib: msgbox_info")
msgbox_error("Example something went wrong 😮!!!", "a2 lib: msgbox_error")
result := msgbox_yesnocancel('Example would you like me to XYZ??', "a2 lib: msgbox_yesnocancel")
msgbox_info("msgbox_yesnocancel result was: " . result, "a2 lib: result")

if msgbox_accepted("Example is that OK?", "Question")
    msgbox_info("that was OK!")
else
    msgbox_info("that was NOT OK!")