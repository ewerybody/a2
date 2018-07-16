#Include  %A_ScriptDir%\..\string_join.ahk

things := ["a", "b", "c"]
string := string_join(things, "||")
msgbox string: %string%
