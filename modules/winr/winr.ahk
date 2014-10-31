;a2VAR 
winrTLDs := ["html", "com", "de", "net", "org", "co.uk"]
;winr

winr() { ;a2CMD
	selection := getSelection()
	selection := trim(selection)
	
	if (selection == "") {
		winrCallDialog()
		return
	}
	; with http:// in the front or filepath that exists
	else if ( RegExMatch(selection, "i)^http://") OR RegExMatch(selection, "i)^https://") OR FileExist(selection) ) {
		Run, %selection%
		return
	}
	; its a web adress: with www. or a TLD at the end? =========
	else if ((SubStr(selection, 1, 4) == "www.") OR (SubStr(selection,-3) == ".com") OR (SubStr(selection,-2) == ".de") OR (SubStr(selection,-3) == ".net") OR (SubStr(selection,-4) == ".html")) {
		Run, http://%selection%
		return
	}
	else {
		MsgBox selection is: "%selection%"
		winrCallDialog()
		sleep, 300
		SendInput, %selection%
	}
}

winrCallDialog() {
	if (A_Language == 0407)
		runWindow = Ausführen ahk_class #32770
	else
		runWindow = Run ahk_class #32770
	Send #r
	WinWaitActive, %runWindow%,, 2
	CoordMode, Mouse, Screen
	MouseGetPos, clq_mousex, clq_mousey
	WinMove, %runWindow%, ,(clq_mousex - 30), (clq_mousey - 10)
}