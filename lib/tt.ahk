; tt() - aka eZtt another tiny tooltip script:
; mouse follow
; timeout
; adding to the tooltip
; changable font
;
; text = the tooltiptext to display, nothing/() kills the tooltip
; timeout = in seconds when the tooltip shall disappear, 0 means never
; add = shall the text be amended to the tooltip or replaced by it
; kill = 1 makes tt sleep until the timeout and throws ExitApp then
; font = fontSize,fontStyle
tt(text="", timeout=0, add=0, kill=0, font="s11,Tahoma")
{
	Global eZttText, eZttID
	eZttDelay := 30

	If text =
		Gosub, eZttOff
	else
	{
		If (add == 1 && eZttText != "")
			eZttText := eZttText "`n" text
		else
			eZttText := text

		if (timeout != 0)
		{
			timeout := timeout * 1000
			SetTimer, eZttOff, -%timeout%
		}

		if not WinExist("ahk_id " eZttID)
		{
			tooltip,% (ttID:=text) ;create tooltip and give it something to find it
			eZttID := WinExist(ttID ahk_class tooltips_class32) ;get ID from it
			HE_SetFont(eZttID, font)

			SetTimer, eZttTimer, %eZttDelay%
		}
		
		if kill
		{
			sleep, timeout
			ExitApp
		}
	}
}

eZttTimer:
	CoordMode, Mouse, Screen
	MouseGetPos, eZttxn, eZttyn
	; if pos and text is the same, do not redraw
	if (eZttxn == eZttx AND eZttyn == eZtty AND eZttText == eZttTextOld)
		return

	Tooltip, %eZttText%
	eZttx := eZttxN
	eZtty := eZttyN
	eZttTextOld := eZttText
Return

eZttOff:
	eZttText =
	eZttID =
	ToolTip
	SetTimer, eZttTimer, Off
Return

; function from majkinetor - http://www.autohotkey.com/forum/viewtopic.php?p=124450#124450
; HE_SetFont( hEdit, "s12 bold, Courier New")
HE_SetFont(hEdit, pFont="") {
   local height, weight, italic, underline, strikeout , nCharSet
   local hFont
   static WM_SETFONT := 0x30

 ;parse font
   italic      := InStr(pFont, "italic")    ?  1    :  0
   underline   := InStr(pFont, "underline") ?  1    :  0
   strikeout   := InStr(pFont, "strikeout") ?  1    :  0
   weight      := InStr(pFont, "bold")      ? 700   : 400

 ;height
   RegExMatch(pFont, "(?<=[S|s])(\d{1,2})(?=[ ,])", height)
   if (height = "")
      height := 10
   RegRead, LogPixels, HKEY_LOCAL_MACHINE, SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontDPI, LogPixels
   height := -DllCall("MulDiv", "int", Height, "int", LogPixels, "int", 72)

 ;face
   RegExMatch(pFont, "(?<=,).+", fontFace)   
   if (fontFace != "")
       fontFace := RegExReplace( fontFace, "(^\s*)|(\s*$)")      ;trim
   else fontFace := "MS Sans Serif"

 ;create font
   hFont   := DllCall("CreateFont", "int",  height, "int",  0, "int",  0, "int", 0
                      ,"int",  weight,   "Uint", italic,   "Uint", underline
                      ,"uint", strikeOut, "Uint", nCharSet, "Uint", 0, "Uint", 0, "Uint", 0, "Uint", 0, "str", fontFace)

   SendMessage,WM_SETFONT,hFont,TRUE,,ahk_id %hEdit%
   return ErrorLevel
}



; testing...
/* #SingleInstance force

#q::Gosub, testEZtt
Return

testEZtt:
	eZtt("lala",0,1,"s20,Arial")
	sleep 1000
	eZtt("vlavlavla",0,1)
	sleep 700
	eZtt("bfbadb",0,0)
	sleep 1000
	eZtt("XXXX",1,1)
Return */