a2_python := _init_get_var("a2_python")
a2_ui_call := _init_get_var("a2_ui_call")
a2_startup_tool_tips := _init_get_var("a2_startup_tool_tips")

PY_VERSION_SHORT := "3.6"

StringLower, a2_startup_tool_tips, a2_startup_tool_tips
if (a2_startup_tool_tips == "true")
    tt("a2ui...", 0.5)

StringLower, a2_ui_call, a2_ui_call
if (SubStr(a2_ui_call, -3) == ".exe")
	this_call := a2_ui_call
else
{
	; check if a2_python exists =======================================================
	if is_absolute_path(a2_python)
	{
		IfNotExist, %a2_python%
		{
			MsgBox, 16, a2_python path inexistent!, The given absolute path for a2_python cannot be found!`n%a2_python%
			ExitApp
		}
		check_pypath := a2_python
	}
	else
	{
		found_list := find_in_env_path(a2_python)
		if found_list.maxIndex() <>
		{
			MsgBox, 16, a2_python path inexistent!, The given relative path for a2_python cannot be found!`n%a2_python%
			ExitApp
		}
		check_pypath := found_list[1]
	}

	; check if a2_python is correct version ============================================
	check_version(check_pypath)
	
	; check if a2_call contains more than the a2app-string =============================
	if (InStr(a2_ui_call, "python.exe") || InStr(a2_ui_call, "pythonw.exe"))
	{
		MsgBox, 16, a2_ui_call contains .exe!, In Settings "a2_ui_call" contrains a python executable name!`nThis was just changed! Make sure it's just the .py file Your want to call!`nBending it to default "a2app.py" now...
		a2_ui_call := "a2app.py" 
	}
	
	this_call := a2_python " " a2_ui_call
}

ui_path = %A_ScriptDir%\..\ui\
Run, %this_call%, %ui_path%

sleep 500



Return ; -----------------------------------------------------------------------------
#include a2init_check.ahk
#include ahklib\tt.ahk


find_in_env_path(filename) {
	results := Array()
	; loop through the environments PATHs separated by ;
	EnvGet, paths, PATH
	Loop, Parse, paths, `;
	{
		this_path := A_LoopField
		; ensure an ending backslash for valid path concatenation
		if (SubStr(A_LoopField, 0) != "\")
			this_path := this_path "\"
		this_path := this_path filename
		IfExist, %this_path%
			results.push(this_path)
	}
	return results
}


is_absolute_path(byref path) {
	SplitPath, path ,,,,, OutDrive
	if (OutDrive == "")
		return false
	else
		return true
}


check_version(check_pypath) {
	global PY_VERSION_SHORT
	FileGetVersion, py_version, %check_pypath%
	if (py_version == "")
	{
		; no version string received. check the readme file for a hint
		SplitPath, check_pypath,, py_dir
		readme_path := py_dir "\README.txt"
		IfExist, %readme_path%
		{
			FileReadLine, readme_line, %readme_path%, 1
			separator_pos := InStr(readme_line, " ",, StartingPos = 0)
			vshort := SubStr(readme_line, separator_pos + 1, 3)
			text := SubStr(readme_line, 1, separator_pos)
			if (vshort != PY_VERSION_SHORT)
			{
				MsgBox, 16, Wrong Python Version?, The Readme next to your found Python executable (%check_pypath%)(%vshort%) does not say "%PY_VERSION_SHORT%"`n`nPlease make sure that a fitting version is found for a2 ui to run on!`nThanks!
				ExitApp
			}
		}
		; I could go into the registry to check for this version ...
	}
	else
	{
		if (SubStr(py_version, 1, 3) != PY_VERSION_SHORT)
		{
			MsgBox, 16, Wrong Python Version?, The found Python executable (%check_pypath%) (%py_version%) does not match version "%PY_VERSION_SHORT%"`n`nPlease make sure that a fitting version is found for a2 ui to run on!`nThanks!
			ExitApp
		}
	}
}
