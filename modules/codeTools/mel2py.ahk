; mel2py.ahk

mel2py()
{
	Selection := getSelection()
	; split by argument indicator "-" and loop each part
	StringSplit, parts, Selection, -
	cmd := ""
	obj := ""
	args := ""
	loop, %parts0%
	{
		p := trim(parts%A_Index%)
		if (p == "")
			Continue
		; make first word command
		if (A_Index == 1)
		{
			cmd := p "( "
			Continue
		}

		StringSplit, thisParts, p, %A_Tab%%A_Space%`r`n
		; last part might be object or part of last argument
		if (A_Index == parts0)
		{
			o := thisParts%thisParts0%
			if SubStr(o,0,1) == ";"
				StringTrimRight, o, o, 1
			if (o == "")
			{
				thisParts0 -= 1
				break
			}

			MsgBox, 4, %o%?, Is this the object?`n%o%
			IfMsgBox Yes
			{
				obj := "'" o "', "
				thisParts0 -= 1
			}
		}

		if (thisParts0 == 1)
		{
			MsgBox thisParts0:%thisParts0%
			args := args p "=1, "
			Continue
		}
		
		if (thisParts0 == 2)
		{
			args := args thisParts1 "=" thisParts2 ", "
			Continue
		}
		
		; with more than 2 parts this must be an array argument
		args := args " " thisParts1 "=[" thisParts2
		loop, %thisParts0%
		{
			tp := thisParts%a_index%
			if (a_index == 1 || a_index == 2 || tp == "")
				Continue

			args := args ", " tp
		}
		args := args "], "

	}
	
	StringTrimRight, args, args, 2

	py := cmd obj args " )"
	tt(py, 2)
	Clipboard := py
}