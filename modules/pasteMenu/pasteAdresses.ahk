
pasteAdresses() {
	global pasteAdressesVars
	for index, value in pasteAdressesVars {
		StringReplace, value, value, `n, %A_Space%, All
		Menu, pasteAdressesMenu, Add, %index%: %value%, pasteAdressesPaste
	}
	Menu, pasteAdressesMenu, Show
	Menu, pasteAdressesMenu, DeleteAll
}

pasteAdressesPaste:
	paste( pasteAdressesVars[A_ThisMenuItemPos] )
Return