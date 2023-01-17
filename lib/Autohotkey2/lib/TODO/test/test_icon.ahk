#Include a2test.ahk
#Include %A_ScriptDir%\..\
#Include ahk_functions.ahk
#Include path.ahk
#Include string.ahk
#Include icon.ahk

for i, ext in ["py", "ahk"]
{
    pth1 := icon_from_type("." ext)
    pth2 := icon_from_type(ext)
    y := assertmsg(pth1 == pth2)
    msg .= ext " icon: " pth1 " " y "`n"
}

MsgBox, %msg%
