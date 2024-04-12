#Include %A_ScriptDir%\..\screen.ahk
screen_get_virtual_size(&x,&y,&w,&h)
msgbox("screen_get_virtual_size:`nx, y: " x "," y ", w, h: " w "," h)

screen_index := screen_get_index(WinExist("A"))
msgbox("screen_index: " screen_index)

workarea := Screen_Workarea()
top := workarea.top
bottom := workarea.bottom
left := workarea.left
right := workarea.right
width := workarea.width
height := workarea.height
msgbox("top: " top " bottom: " bottom "`nleft: " left " right: " right "`nwidth: " width " height: " height)

Loop(MonitorGetCount())
{
    MonitorGetWorkArea(A_Index, &Left, &Top, &Right, &Bottom)
    MsgBox("Monitor " A_Index "`nLeft: " Left " Top: " Top " Right: " Right " Bottom " Bottom)
}