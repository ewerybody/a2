; CalculAid - calculAid.ahk
; author: eRiC
; created: 2015 10 10
;
; nice :/ on win10 although you call calc.exe the calculator process executable will be:
; "ApplicationFrameHost.exe" and the class: "ApplicationFrameWindow". Thanks MS! This can be
; ANYTHING!!! OK the title is still "Calculator" but only on an english system.
; So basically we need logic for all of that because nothing
; is for sure. Furthermore that also means that the Close-hetkeys we wanna setup in a2ui will need
; win-version and language specific scope identifyers. In the end such a function will be quite
; nice to have in a2 anyway.

calculAid_open() {
    tt("CalculAid...", 1)
    global calculAid_openAtCursor, calculAid_AlwaysOnTop
    sel := getSelection()
    RegExMatch(sel, "[0-9.,+/*=-]+", numbers)
    ;tt(numbers)
    
    Run, calc.exe,, UseErrorLevel, calcPID
    
	If calculAid_openAtCursor
	{
        ;tt("waiting for pid:" calcPID " ...", 2, 1)
		WinWait, ahk_pid %calcPID%,, 2
        ;win10Calc := "Calculator ahk_class ApplicationFrameWindow ahk_exe ApplicationFrameHost.exe"
        ;win7Calc := "Calculator ahk_class CalcFrame ahk_exe calc.exe"
        ;WinWait, %win7Calc%,, 2
        sleep, 50
        ;tt("Window found! " calcPID, 1)
		CoordMode, Mouse, Screen
		MouseGetPos, clq_mousex, clq_mousey
		;position the windowtitle under the cursor so one can move it instantly:
        WinMove, %win7Calc%,, (clq_mousex - 30), (clq_mousey - 10)
		;WinMove, (clq_mousex - 30), (clq_mousey - 10), %win10Calc%
	}

	If calculAid_AlwaysOnTop
	{
		WinWait, ahk_pid %calcPID%,, 2
		WinSet, AlwaysOnTop, On, ahk_pid %calcPID%
	}
}
