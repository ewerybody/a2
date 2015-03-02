pasteDates() {
	german:= A_DD "." A_MM "." A_YYYY
	slash := A_DD "/" A_MM "/" A_YYYY
	short := A_YYYY A_MM A_DD
	words := A_DD ". " A_MMMM " " A_YYYY
	Menu, pasteDatesMenu, Add, %german%, pasteDatesPaste
	Menu, pasteDatesMenu, Add, %slash%, pasteDatesPaste
	Menu, pasteDatesMenu, Add, %short%, pasteDatesPaste
	Menu, pasteDatesMenu, Add, %words%, pasteDatesPaste
	Menu, pasteDatesMenu, Add, %A_now%, pasteDatesPaste
	Menu, pasteDatesMenu, Show
	Menu, pasteDatesMenu, DeleteAll
}

pasteDatesPaste:
	paste( A_ThisMenuItem, sleepTime=20 )
Return