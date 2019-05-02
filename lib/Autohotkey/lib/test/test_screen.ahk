#Include  %A_ScriptDir%\..\screen.ahk
screen_get_virtual_size(x,y,w,h)
msgbox screen_get_virtual_size:`nx, y: %x%, %y%, w, h: %w%, %h%

screen_index := screen_get_index(WinExist("A"))
msgbox screen_index: %screen_index%

workarea := new Screen_Workarea()
top := workarea.top
msgbox top1: %top%
