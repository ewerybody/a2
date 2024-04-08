#Include %A_ScriptDir%\..\uri.ahk
#Include a2test.ahk


ec := "https%3A%2F%2Fexample.com%2Fcontact%2Frf%2Fcontact.jsp"
dc := uri_decode(ec)
e2 := uri_encode(dc)
e3 := uri_url_encode(dc)
e4 := uri_encode(dc, "[0-9a-zA-Z;?@,&=+$#.]")
msg .= "ec: " ec "`nuri_decode(ec): " dc "`nuri_encode(dc): " e2
msg .= "`nuri_url_encode(dc): " e3 "`nuri_encode 2: " assertmsg(ec == e4) "`n" e4
MsgBox(msg)