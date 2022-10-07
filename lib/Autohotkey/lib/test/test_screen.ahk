#Include %A_ScriptDir%\..\screen.ahk
screen_get_virtual_size(x,y,w,h)
msgbox screen_get_virtual_size:`nx, y: %x%, %y%, w, h: %w%, %h%

screen_index := screen_get_index(WinExist("A"))
msgbox screen_index: %screen_index%

workarea := new Screen_Workarea()
top := workarea.top
bottom := workarea.bottom
left := workarea.left
right := workarea.right
width := workarea.width
height := workarea.height
msgbox top: %top% bottom: %bottom%`nleft: %left% right: %right%`nwidth: %width% height: %height%

SysGet, moni_count, MonitorCount
Loop, %moni_count%
{
    SysGet, moni_stuff, Monitor , %A_Index%
    MsgBox, Monitor %A_Index%`nLeft: %moni_stuffLeft% Top: %moni_stuffTop% Right: %moni_stuffRight% Bottom %moni_stuffBottom%.
}