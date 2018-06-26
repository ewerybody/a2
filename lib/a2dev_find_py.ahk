a2_PY_VERSION_SHORT := "3.6"

a2dev_find_py () {
    py_key = HKEY_CURRENT_USER\Software\Python\PythonCore\%a2_PY_VERSION_SHORT%\InstallPath
    RegRead, a2_python, %py_key%, ExecutablePath
    
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
    
    return check_pypath
}


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
	global a2_PY_VERSION_SHORT
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
			if (vshort != a2_PY_VERSION_SHORT)
			{
				MsgBox, 16, Wrong Python Version?, The Readme next to your found Python executable (%check_pypath%)(%vshort%) does not say "%a2_PY_VERSION_SHORT%"`n`nPlease make sure that a fitting version is found for a2 ui to run on!`nThanks!
				ExitApp
			}
		}
	}
	else
	{
		if (SubStr(py_version, 1, 3) != a2_PY_VERSION_SHORT)
		{
			MsgBox, 16, Wrong Python Version?, The found Python executable (%check_pypath%) (%py_version%) does not match version "%a2_PY_VERSION_SHORT%"`n`nPlease make sure that a fitting version is found for a2 ui to run on!`nThanks!
			ExitApp
		}
	}
}
