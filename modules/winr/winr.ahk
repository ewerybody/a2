;a2VAR 
winrTLDs := ["html", "com", "de", "net", "org", "co.uk"]
;winr

winr() { ;a2CMD
    global winrProjectPaths
	selection := getSelection()
	selection := trim(selection)
	
	if ( selection == "" ) {
		winrCallDialog()
	}
	else if FileExist(selection) {
        tt("path exists...",0.5)
		winrCatchedCallRun(selection)
	}
	; has http:// in the front
	else if ( RegExMatch(selection, "i)^http://") OR RegExMatch(selection, "i)^https://") ) {
		tt("web address...",0.5)
        winrCatchedCallRun(selection)
	}
	; its a web address: with www. or a TLD at the end? =========
	else if ( (SubStr(selection, 1, 4) == "www.") OR (SubStr(selection,-3) == ".com") OR (SubStr(selection,-2) == ".de") OR (SubStr(selection,-3) == ".net") OR (SubStr(selection,-4) == ".html") ) {
        tt("web address...",0.5)
        winrCatchedCallRun("http://" selection)
	}
	else {
        ; loop set up project paths, if combination with selection fits: run it
        StringReplace, slashed, selection, /, \, All
        for i, ppath in winrProjectPaths {
            ppath = %ppath%\%slashed%
            if FileExist(ppath) {
                tt("project path exists...",0.5)
                winrCatchedCallRun(ppath)
                Return
            }
        }

        tt("Does not exist!`nI don't know what todo with your selection...", 1)
        winrCallDialog()
        sleep, 300
        SendInput, %selection%
    }
}

winrCallDialog() {
	runWindow = Run ahk_class #32770
	Send #r
	WinWaitActive, %runWindow%
	CoordMode, Mouse, Screen
	MouseGetPos, clq_mousex, clq_mousey
	WinMove, %runWindow%, ,(clq_mousex - 30), (clq_mousey - 10)
}

winrCatchedCallRun(ppath) {
    Run, %ppath%,, UseErrorLevel
    if ErrorLevel {
        cmd = explorer.exe /select,"%ppath%"
        Run, %cmd%
        tt("but I cound not 'Run' it!`nExploring to ...:", 1.5, 1)
    }
}