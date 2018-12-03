path_is_absolute(byref path) {
	SplitPath, path ,,,,, OutDrive
	if (OutDrive == "")
		return false
	else
		return true
}

path_dirname(byref path) {
    SplitPath, path,, OutDir
    Return OutDir
}

path_basename(byref path) {
    SplitPath, path, OutFileName
    Return OutFileName
}

path_is_dir(byref path) {
    if (InStr(FileExist(path), "D"))
        return true
    else
        return false
}
