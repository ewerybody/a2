
getSelection( clipWaitTime=0.5 )
{
	SavedClipboard := ClipboardAll
	Clipboard =
	Sleep, 0

	; also watch for the process-executable instead of just window title:
	WinGetClass, Class, A
	WinGet, this_process, ProcessName, ahk_class %Class%

	; sending keystroke Ctrl+C in maya can cause a "scene clipboard save" which can be heavy
	; to avoid this we go sure we are in the text editor window of maya
	if (this_process == "maya.exe")
	{
		WinGetTitle, this_title, A
		if (this_title != "Script Editor")
			Return ""
	}

	;Send, {Blind}%resetModifiers%^c%restoreModifiers%
	if (this_process == "Photoshop.exe")
	{
		SetKeyDelay, 20, 20
		SendEvent, {Ctrl down}^c{Ctrl up}
	}
	Else If Class in PuTTY,ConsoleWindowClass,ytWindow
		Send, {ENTER}
	Else
		Send, {Ctrl down}^c{Ctrl up}

	If clipWaitTime <>
	{
		If copyAsText = 0
			ClipWait, %clipWaitTime%, 1
		Else
			ClipWait, %clipWaitTime%
	}
	Sleep,0

	Selection := Clipboard
	Clipboard := SavedClipboard

	Return Selection
}


; good ol getSelection function from ac'tivAid
; copyOnly=1 to actually fill the clipboard
aagetSelection( copyAsText=1, copyOnly=0, clipWaitTime=0.5 )
{
	global Selection, SavedClipboard, NoOnClipboardChange
	NoOnClipboardChange = 1

	; also watch for the process-executable instead of just window title:
	WinGetClass, Class, A
	WinGet, this_process, ProcessName, ahk_class %Class%

	; sending keystroke Ctrl+C in maya can cause a "scene clipboard save" which can be heavy
	; to avoid this we go sure we are in the text editor window of maya
	if (this_process == "maya.exe")
	{
		WinGetTitle, this_title, A
		if (this_title != "Script Editor")
		{
			Selection := ""
			Return
		}
	}

	;Send, {Blind}%resetModifiers%^c%restoreModifiers%
	if (this_process == "Photoshop.exe")
	{
		SetKeyDelay, 20, 20
		SendEvent, {Ctrl down}^c{Ctrl up}
	}
	Else If Class in PuTTY,ConsoleWindowClass,ytWindow
		Send, {ENTER}
	Else
		Send, {Ctrl down}^c{Ctrl up}

	if (this_process == "Photoshop.exe")
	{
		Gui, 99:+ToolWindow
		Gui, 99:Show, x-1000 y-1000 w10 h10
	}

	If clipWaitTime <>
	{
		If copyAsText = 0
			ClipWait, %clipWaitTime%, 1
		Else
			ClipWait, %clipWaitTime%
	}
	Sleep,0

	if (this_process == "Photoshop.exe")
	{
		Sleep,10
		Gui, 99:Destroy
	}

	If copyAsText = 1
		Selection := Clipboard
	;Else If copyAsText in Unicode,UTF8,UTF-8
	;{
	;	Transform, Selection, Unicode
	;	;msgbox, % Ansi2UTF8(UTF82Ansi(Selection)) "`n" Selection
	;	If (Ansi2UTF8(UTF82Ansi(Selection)) = Selection)
	;		Selection := Clipboard
	;}
	Else
		Selection := ClipboardAll

	If copyOnly = 0
	{
		Sleep, 20
		Clipboard := SavedClipboard
	}
	Sleep,0

	NoOnClipboardChange =

	If copyAsText = 1
		Return Selection
}

; to remove whitespace from strings start + end
trim(string)
{
	start := 1
	stringLen, end, string
	loop, %end% ; fix the start
	{
		l := SubStr(string, A_Index, 1)
		if (l != A_Space && l != A_Tab && l != "`n" && l != "`r")
		{
			start := A_Index
			break
		}
	}
	string := SubStr(string, start)
	stringLen, end, string
	loop, %end% ; fix the end
	{
		i := - A_Index + 1
		l := SubStr(string, i, 1)
		if (l != A_Space && l != A_Tab && l != "`n" && l != "`r")
		{
			end := A_Index - 1
			break
		}
	}
	StringTrimRight, string, string, %end%
	return string
}


; WIP: Which version do you like more?!?!
; strips whitespace from start and end of a string:
strip(byref inputString)
{
	; if first char is space, tab or linefeed, remove it and look again:
	c := SubStr(inputString, 1, 1)
	if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
	{
		StringTrimLeft, inputString, inputString, 1
		strip(inputString)
	}
	; now last character:
	c := SubStr(inputString, 0)
	if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
	{
		StringTrimRight, inputString, inputString, 1
		strip(inputString)
	}
}

paste( byref inputString, sleepTime=50 ){
	SavedClipboard := ClipboardAll
	Clipboard =
	Sleep, %sleepTime%
	Clipboard := inputString
	ClipWait, 1
	Send, {Ctrl down}^v{Ctrl up}
	Clipboard := SavedClipboard
}

; returns a real array of split items
; TODO: this is built-in already! Replace with StrSplit() !
split( byref string, sep=" "){
    ;StringSplit
    splitList := []
    Loop, Parse, string, %sep%
		splitList.insert(A_LoopField)
	return splitList
}

; looks up the items of an array object
; returns index of search string if found
; returns 0 otherwise
inArray(byref search, byref array) {
    ;for i, value in array {
    Loop % array.MaxIndex() {
        if (search == array[A_Index])
            Return A_Index
    }
    Return 0
}

; takes simple array object
; returns all its pieces concatenated with the sep string
join(byref array, sep="`n") {
    text := array[1]
    for i, value in array {
        if (i != 1)
            text := text sep value
    }
    Return text
}
; checks for some aspects to assume that the given string is a URL
; TODO: this can probably be done much much better!!!...
isURL(byref str)
{
	; look if the start of the string is url like
	if (SubStr(str,1,7) == "http://" || SubStr(str,1,8) == "https://" || SubStr(str,1,4) == "www.")
		return true
	; now the end of the string
	if (SubStr(str,-3,4) == ".htm" || SubStr(str,-4,5) == ".html")
		return true
	; now if inbetween are TLDs like .com, .de, .co.uk ...
	else
	{
		dotpos := InStr(str,".")
		sub := SubStr(str,dotpos,3)
		if (sub == ".de" || sub == ".at" || sub == ".ch")
			return true
		sub := SubStr(str,dotpos,4)
		if (sub == ".com" || sub == ".org" || sub == ".net")
			return true
		if (SubStr(str,dotpos,6) == ".co.uk")
			return true
	}
	return false
}
