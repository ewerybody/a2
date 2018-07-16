file_is_absolute_path(byref path) {
	SplitPath, path ,,,,, OutDrive
	if (OutDrive == "")
		return false
	else
		return true
}
