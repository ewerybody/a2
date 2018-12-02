#Include  %A_ScriptDir%\..\string.ahk

things := ["a", "b", "c"]
string := string_join(things, "||")
msgbox string: %string%
