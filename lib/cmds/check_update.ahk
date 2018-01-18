; check_update - Returns 1 if there is a different Autohotkey version online!
update_url := "https://autohotkey.com/download/1.1/version.txt"
whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
whr.Open("GET", update_url, false)
whr.Send()
whr.WaitForResponse()
version := whr.ResponseText
if (version == A_AhkVersion)
    FileAppend, 0, *
else
    FileAppend, 1, *
