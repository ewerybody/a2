pasteColor()
{
	hexColor := Clipboard
	
	; Check different versions of color Dialogs
	WinGet, this_id, ID, A
	; Color tool hast Static13/14/15 as &Red:/&Green:/Bl&ue: labels  ... or Static7/8/9
	StaticNrs := [ [7, "&Red:","&Green:","&Blue:"] , [13, "&Red:","&Green:","&Blue:"], [13,"&Red:",	"&Green:","Bl&ue:"] ]
	isColorDialog := 0
	Loop % StaticNrs.MaxIndex()
	{
		labels := ["","",""]
		i := A_Index
		Loop 3 {
			name := "Static" (StaticNrs[i][1] + A_Index - 1)
			ControlGetText, label, %name%, ahk_id %this_id%
			labels[A_Index] := label
		}
		If (labels[1] == StaticNrs[i][2] && labels[2] == StaticNrs[i][3] && labels[3] == StaticNrs[i][4]) {
			isColorDialog := 1
			break
		}
	}
	if isColorDialog
		tt("Lets Paste Colors!...")
	else {
		tt("This is no Color dialogue is it?",1)
		return
	} ; Check done we probably have a color dialog

	v1 := hexColor2int(hexColor, 0)
	v2 := hexColor2int(hexColor, 1)
	v3 := hexColor2int(hexColor, 2)
	; and Edit4/5/6 as according fields
	Loop, 3
	{
		ctrl := "Edit" (A_Index + 3)
		value := v%A_Index%
		tt(value,,1)
		ControlSetText, %ctrl%, %value%, ahk_id %this_id%
	}
	tt("okithxbye",1,1)
}

hexColor2int(hex, index)
{
	start := (index * 2) + 1
	Num := "0x" SubStr(hex, start, 2)

	A_FI := A_FormatInteger
	SetFormat, Integer, Decimal
	Num += 0
	SetFormat, Integer, %A_FI%
	Return Num
}