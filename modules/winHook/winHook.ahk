DetectHiddenWindows, On
OnExit, winHookQUIT

hWinEventHook := winHook_init("WINEVENT", sSearchList)
Return

winHookQUIT:
	winHook_StopChecking(hWinEventHook)
	ExitApp
Return

winHookWINEVENT(sEvent, hWnd) {
	MsgBox, %sEvent%: %hWnd%
}

; LIB :: ewinhook.ahk
; ~~~~~~~~~~~~~~~~~~~
; This library implements a hook on EVENT_OBJECT_CREATE and EVENT_OBJECT_DESTROY windows events. It makes it possible to catch
; these events being notified through a callback procedure for each required window.
; ------------------------------------------------------------------------------------------------------------------------------
; PUBLIC  FUNCTIONS: winHook_init | winHook_StopChecking
; PRIVATE FUNCTIONS: prv_ewinhook_HookProc
; ------------------------------------------------------------------------------------------------------------------------------
; cyrusza   - http://ciroprincipe.info

/*
--------------------------------------------------------------------------------------------------------------------------------
INSTRUCTIONS:
--------------------------------------------------------------------------------------------------------------------------------
To use this library, create a function to receive and manage notifications and pass it to the winHook_init as
a string, together with the list of windows classes/titles (newline separated) that you need to catch. The function must accept
2 parameters: a string containing the event description and the handle of the involved window. At the end of the operations,
the winHook_StopChecking function must be called to unregister the hook.

This is an example of the code needed to be notified of the followings:
1. All AutoHotkey main windows.
2. All Notepad2 windows.
3. Windows that have the words "Firefox, Windows and Paint.NET" in their title.

[code]
#Persistent
DetectHiddenWindows, On
OnExit, QUIT

sSearchList =
(
ahk_class AutoHotkey
ahk_class Notepad2
Firefox
Windows
Paint.NET
)

hWinEventHook := winHook_init("WINEVENT", sSearchList)
Return

QUIT:
winHook_StopChecking(hWinEventHook)
ExitApp

WINEVENT(sEvent, hWnd) {
	MsgBox, %sEvent%: %hWnd%
}
[/code]
--------------------------------------------------------------------------------------------------------------------------------
*/

/*
--------------------------------------------------------------------------------------------------------------------------------
FUNCTION: winHook_init
--------------------------------------------------------------------------------------------------------------------------------
This function initializes the hook and returns a handle to it. Can be called at any times to update the windows search list.

PARAMETERS:
~~~~~~~~~~~
sCallback	- Name of the function that will receive the notifications.
sSearchList	- Newline separated list that will contain windows classes or titles to be searched by the hooking procedure.
				To search for a class, use "ahk_class CLASSNAME"
				To search for a title, use "TITLE"
				Window titles search will behave like "SetTitleMatchMode, 2"
--------------------------------------------------------------------------------------------------------------------------------
SYSTEM CALLS AND STRUCTURES:
--------------------------------------------------------------------------------------------------------------------------------
CoInitialize	- http://msdn.microsoft.com/en-us/library/windows/desktop/ms678543%28v=vs.85%29.aspx
SetWinEventHook	- http://msdn.microsoft.com/en-us/library/windows/desktop/dd373640%28v=vs.85%29.aspx
--------------------------------------------------------------------------------------------------------------------------------
*/
winHook_init(sCallback, sSearchList="") {
	Global ewinhook_sCallback  := sCallback
		, ewinhook_sClassList := ""
		, ewinhook_sTitleList := ""
		 
	Static ewinhook_hWinEventHook
	If (!ewinhook_hWinEventHook)
		DllCall( "CoInitialize", UInt, 0 )
		, ewinhook_hWinEventHook := DllCall( "SetWinEventHook"
									,  UInt, 0x8000			; EVENT_OBJECT_CREATE
									,  UInt, 0x8001			; EVENT_OBJECT_DESTROY
									,  UInt, 0
									,  UInt, RegisterCallback("prv_ewinhook_HookProc")
									,  UInt, 0
									,  UInt, 0
									,  UInt, 0				 ; WINEVENT_OUTOFCONTEXT
									,  UInt )

	; wip this parses the sSearchList-string,
	; sorts ahk_class occurences to ewinhook_sClassList and others to ewinhook_sTitleList
	; what the crap!?
	Loop, PARSE, sSearchList, `n
	{
		If (InStr(A_LoopField, "ahk_class"))
			ewinhook_sClassList .= RegExReplace(A_LoopField, "ahk_class ") . "`n"
		Else
			ewinhook_sTitleList .= A_LoopField . "`n"
	}
	Return ewinhook_hWinEventHook
}

/*
--------------------------------------------------------------------------------------------------------------------------------
FUNCTION: winHook_StopChecking
--------------------------------------------------------------------------------------------------------------------------------
This function deinitializes the hook.

PARAMETERS:
~~~~~~~~~~~
hWinEventHook   - Name of the function that will receive the notifications.
--------------------------------------------------------------------------------------------------------------------------------
SYSTEM CALLS AND STRUCTURES:
--------------------------------------------------------------------------------------------------------------------------------
UnhookWinEvent	- http://msdn.microsoft.com/en-us/library/windows/desktop/dd373671%28v=vs.85%29.aspx
CoUninitialize	- http://msdn.microsoft.com/en-us/library/windows/desktop/ms688715%28v=vs.85%29.aspx
--------------------------------------------------------------------------------------------------------------------------------
*/
winHook_StopChecking(hWinEventHook) {
	DllCall( "UnhookWinEvent", UInt, hWinEventHook )
	DllCall( "CoUninitialize" )
}

/*
--------------------------------------------------------------------------------------------------------------------------------
FUNCTION: prv_ewinhook_HookProc
--------------------------------------------------------------------------------------------------------------------------------
This is the hooking procedure that will be called by the system when the events are triggered. It checks the windows objects and
calls the callback if it finds a match.

PARAMETERS:
~~~~~~~~~~~
hWinEventHook   - Handle to the current hook.
event			- Event type. Can be EVENT_OBJECT_CREATE = 0x8000 or EVENT_OBJECT_DESTROY = 0x8001.
hWnd			- Handle to the window that triggered the event.
idObject		- Id of the object associated with the event.
idChild			- Identifies if the event was triggered by the object or by a child element of the object.
dwEventThread   - Identifies the thread that generated the event or that owns the window.
dwmsEventTime   - Times in ms that the event was generated.
--------------------------------------------------------------------------------------------------------------------------------
*/
prv_ewinhook_HookProc(hWinEventHook, event, hWnd, idObject, idChild, dwEventThread, dwmsEventTime) {
	Global ewinhook_sCallback
		 , ewinhook_sClassList
		 , ewinhook_sTitleList

	WinGetClass, sClass, ahk_id %hWnd%
	WinGetTitle, sTitle, ahk_id %hWnd%
	WinGet, sProcess, ProcessName, ahk_id %hWnd%

	bFound := 0
	Loop, PARSE, ewinhook_sClassList, `n
		If (A_LoopField && InStr(sClass, A_LoopField))
			bFound := 1
	Loop, PARSE, ewinhook_sTitleList, `n
		If (A_LoopField && InStr(sTitle, A_LoopField))
			bFound := 1
		   
	If (bFound)
		%ewinhook_sCallback%((event == 0x8000) ? "Created" : "Destroyed", hWnd)
}