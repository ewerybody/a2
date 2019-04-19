#Include  %A_ScriptDir%\..\screen.ahk

x := 0
y := 0
w := 0
h := 0
msgbox screen_get_virtual_size before:`nx, y: %x%, %y%, w, h: %w%, %h%
screen_get_virtual_size(x,y,w,h)
msgbox screen_get_virtual_size after:`nx, y: %x%, %y%, w, h: %w%, %h%

screen_index := screen_get_index(WinExist("A"))
msgbox screen_index: %screen_index%
