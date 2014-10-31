getControlWithFocus:
	WinGet, this_id, ID, A

	ControlGetFocus, OutputVar, ahk_id %this_id%
	if ErrorLevel
		MsgBox, The target window doesn't exist or none of its controls has input focus.
	else
		ControlGetText, value, %OutputVar%, ahk_class CryEditorClass
		MsgBox, Control with focus = %OutputVar%`nvalue:%value%
Return