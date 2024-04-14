; check_update - Returns 1 if there is a different Autohotkey version online!
update_url := "https://autohotkey.com/download/2.0/version.txt"
whr := ComObject("WinHttp.WinHttpRequest.5.1")
whr.Open("GET", update_url, false)
whr.Send()
whr.WaitForResponse()
version := whr.ResponseText
if (version == A_AhkVersion)
    result := 0
else
    result := 1

FileAppend(result, '*')