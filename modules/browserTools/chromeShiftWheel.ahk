#IfWinActive, ahk_class Chrome_WidgetWin_1
+WheelUp::Send, {Browser_Forward}
+WheelDown::Send, {Browser_Back}