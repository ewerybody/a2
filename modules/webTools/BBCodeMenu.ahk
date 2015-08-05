; URL erzeugt links im style [URL=http://safdsadf]text[/URL]
; wenn ein URL im Clipboard ist wird dieser sofort in den href geschrieben
; nix markiert: kommt der cursor dann in die >< ansonsten kommt das markierte dazwischen
; ist ein link markiert wird der auch ins href geschrieben und der cursor zw. >< positioniert

BBCodeMenu(){
    ; add menu entries on demand...
	Menu, BBCodeMenu, Add, IMG, BBCodeMenuHandler
	Menu, BBCodeMenu, Add, URL, BBCodeMenuHandler
	Menu, BBCodeMenu, Add, QUOTE, BBCodeMenuHandler
    Menu, BBCodeMenu, Add, B, BBCodeMenuHandler
	Menu, BBCodeMenu, Show
	Menu, BBCodeMenu, DeleteAll
}

BBCodeMenuHandler:
	BBCodeMenuHandler() 
Return
BBCodeMenuHandler() {
	sel := getSelection()
	if (A_ThisMenuItem == "URL")
	{
		If (isURL(sel))
		{
			tt("selection is URL",1)
			paste( "[URL=" sel "][/URL]" )
			SendInput, {Left 6}
		}
		; if clipboard already contains a URL put that in the [URL= and the selection between ][/URL]
		Else If (isURL(Clipboard))
		{
			tt("Clipboard is URL",1)
			code := "[URL=" Clipboard "]" sel "[/URL]"
			paste(code)
		}
		; otherwise just put the selected into the ><
		Else
		{
			tt("otherwise...",1)
			code := "[URL=]" sel "[/URL]"
			paste(code)
			StringLen, hLen, sel
			hLen += 7
			SendInput, {Left %hLen%}
		}
	}
	else {
		code := "[" A_ThisMenuItem "]" sel "[/" A_ThisMenuItem "]"
		paste(code)
	}
}