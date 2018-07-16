files_in_clipboard() {
    files := StrSplit(Clipboard, "`r`n")
    is_files := true
    for i, item in files {
        if !FileExist(item) {
            is_files := false
            Break
        }
    }

    if (is_files)
        return files
}
