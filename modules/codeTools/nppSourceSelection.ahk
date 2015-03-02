nppSourceSelection() {
	selection := getSelection()

	; get the type of script --------------------
	; get window id
	WinGet, notepad_id, ID, A
	; get text from the statusline
	ControlGetText, statusText, msctls_statusbar321, ahk_id %notepad_id%
	If statusText =
		ControlGetText, statusText, msctls_statusbar322, ahk_id %notepad_id%
	
	if InStr(statusText,"AHK")
		scriptType = ahk
	else if InStr(statusText,"Python")
		scriptType = py
	else if InStr(statusText,"- mel")
		scriptType = mel
    else if InStr(statusText, "Nullsoft Scriptable Install System")
        scriptType = nsi

	; get the filename if there is any ----------
	WinGetActiveTitle, fileName
	if (SubStr(fileName,1,1) = "*")
		StringTrimLeft, fileName, fileName, 1

    x := InStr(fileName, " - Notepad++") - 1
	StringLeft, fileName, fileName, %x%
    
	; MAYA scripts =================================================================================
	; WiP this Maya part is currently not working in a2 ... needs a command port in Maya and a
    ; working python evironment
	If (scriptType == "mel") OR (scriptType == "py")
	{
		tt("Sorry - Maya mel and python part is currently WIP here...",1)
	}
	; AUTOHOTKEY scripts ===========================================================================
	Else If (scriptType = "ahk")
	{
		If (selection != "") ; save selection to  and call autohotkey.exe with selectionSource.ahk
		{
			tt("selection",0,1)
			file = %A_Temp%\AHKtest.ahk

			FileDelete %file%
			FileAppend, #SingleInstance force`n, %file%
			FileAppend, %selection%, %file%
			tt("running with Autohotkey...",1,1)
			Run, %file%
			sleep 500
		}
		Else
		{
			tt("whole file`nrunning with Autohotkey...",1,1)
			SplitPath, fileName, fileShortName, fileDir
			Run, %fileShortName%, %fileDir%
			sleep 500
		}
	}
	Else If (scriptType = "nsi")
	{
        tt("NSIS`n" fileName,1)
        ;NSISpath := A_ProgramFiles "\NSIS\NSIS.exe"
        NSISpath := A_ProgramFiles "\NSIS\makensisw.exe"
        IfExist %NSISpath%
            Run, "%NSISpath%" "%fileName%"
        Else
            MsgBox NSISpath: %NSISpath% Does NOT Exist!
    }
	Else
    {
		MsgBox Hi! The scriptType is neither PYTHON, MEL or Autohotkey, what shall I do?`n"%statusText%"?
        tt()
    }
}