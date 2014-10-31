; simpleList.ahk
; a tiny tool to show a number of entrys you can search in


; WIP should be rewritten Autohotkey_L style!


StringSplit, itemArray, items, |

CoordMode, Caret, Screen
xpos := A_CaretX + 5
ypos := A_CaretY - 27

Gui, -MinimizeBox -MaximizeBox +Resize
Gui, Font, s11, Tahoma
Gui, Add, Edit,x0 y0 w300 r1 vsimpleListEdit gDoSearch, %text%
Gui, Add, ListBox, y+0 w300 r9 vsimpleListList AltSubmit gItemClicked, %items%
GuiControl, Choose, simpleListList, 1
Gui, Show, x%xpos% y%ypos% w300 h192, simpleList

SetTimer, ExitIfFocusLost, 250

Return

GuiSize:
   Anchor("simpleListList", "hw", true)
   Anchor("simpleListEdit", "w", true)
Return

ExitIfFocusLost:
	IfWinNotActive, simpleList
	ExitApp
return

Tab::
Down::changeSelItemIndex(1)
Up::changeSelItemIndex(-1)
PgDn::changeSelItemIndex(5)
PgUp::changeSelItemIndex(-5)
~Home::changeSelItemIndex(0)
~End::changeSelItemIndex(888)

changeSelItemIndex(amount)
{
	global newArray0
	global itemArray0
	GuiControlGet, simpleListList
	GuiControlGet, simpleListEdit
	;get from all or searched list:
	If (simpleListEdit != "")
		numAllItems := newArray0
	Else
		numAllItems := itemArray0

	; hop to the start or end if nothing written yet:
	if (amount == 0)
		if (simpleListEdit == "")
			newPos := 1
		Else
			return
	else if (amount == 888)
		if (simpleListEdit == "")
			newPos := numAllItems
		Else
			return
	; else browse the list:
	Else
	{
		newPos := simpleListList + amount
		if newPos < 1
			newPos := numAllItems
		else if newPos > %numAllItems%
			newPos := 1
	}

	GuiControl, Choose, simpleListList, %newPos%
}

Enter::
	GuiControlGet, simpleListList
	GuiControlGet, simpleListEdit
	Gui, Destroy

	;get the item from the full or the searched list:
	selItem =
	If (simpleListEdit != "")
		selItem := newArray%simpleListList%
	Else
		selItem := itemArray%simpleListList%

	;send only the first item before space:
	IfInString, selItem, %A_Space%
	{
		StringSplit, itemParts, selItem , (%A_Space%)
		;MsgBox itemParts1:%itemParts1%`nitemParts2:%itemParts2%
		selItem := itemParts1
	}

	tmp := ClipboardAll
	Clipboard := extra selItem
	Send {Right}^v
	Clipboard := tmp
	ExitApp
Return

GuiEscape:
GuiClose:
ExitApp

ItemClicked:
	GuiControlGet, simpleListList
	if (A_GuiEvent == "DoubleClick")
		Gosub, Enter
Return

DoSearch:
	GuiControlGet, simpleListEdit
	newList =
	newArray0 := 0
	; if string is empty show the full list:
	if (simpleListEdit == "")
	{
		GuiControl,, simpleListList, |%items%
		GuiControl, Choose, simpleListList, 1
		Return
	}

	; otherwise browse through the initial list:
	Loop, %itemArray0%
	{
		thisItem := itemArray%A_Index%
		If (InStr(thisItem, simpleListEdit) AND simpleListEdit != "")
		{
			newList = %newList%|%thisItem%
			newArray0++
			newArray%newArray0% := thisItem
		}
	}

	GuiControl,, simpleListList, %newList%
	GuiControl, Choose, simpleListList, 1
Return