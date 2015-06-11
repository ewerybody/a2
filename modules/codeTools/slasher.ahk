; codeTools - slasher.ahk
; author: eric
; created: 2015 6 11

slasher() {
    Menu, slasher_menu, Add, 1 \ <> / toggle back/forward, slasher_menu_handler
    Menu, slasher_menu, Add, 2 \ > \\ double backslashes, slasher_menu_handler
    Menu, slasher_menu, Add, 3 \\ > \ single backslashes, slasher_menu_handler
    
	Menu, slasher_menu, Show
	Menu, slasher_menu, DeleteAll
}

slasher_menu_handler:
    Selection := getSelection()
    if (A_ThisMenuItemPos == 1) {
        IfInString, Selection, /
            outstr := StrReplace(Selection, "/" , "\")
        else
        IfInString, Selection, \
            outstr := StrReplace(Selection, "\" , "/")
    }
    else if (A_ThisMenuItemPos == 2)
        outstr := StrReplace(Selection, "\" , "\\")
    else if (A_ThisMenuItemPos == 3)
        outstr := StrReplace(Selection, "\\" , "\")
    paste(outstr)
Return