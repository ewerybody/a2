#Include %A_ScriptDir%\..\ahk_functions.ahk
#Include a2test.ahk

msg .= "StrLower: " StrLower("StrLower") " StrUpper: " StrUpper("StrUpper") " StrTitle: " StrTitle("str title")

MsgBox, %msg%