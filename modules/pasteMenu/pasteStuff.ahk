
pasteStuff() {
	global pasteStuffVars
	for index, value in pasteStuffVars {
		StringReplace, value, value, `n, %A_Space%, All
		Menu, pasteStuffMenu, Add, %index%: %value%, pasteStuffPaste
	}
	Menu, pasteStuffMenu, Show
	Menu, pasteStuffMenu, DeleteAll
}

pasteStuffPaste:
	paste( pasteStuffVars[A_ThisMenuItemPos] )
Return