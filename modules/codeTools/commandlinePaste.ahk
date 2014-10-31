; commandLinePaste
#IfWinActive, ahk_class ConsoleWindowClass
^v::SendInput, %Clipboard%