nppExploreTo() {
    WinGetTitle, filepath, A
    endPos := InStr(filepath, " - Notepad++") - 1
    filepath := SubStr(filepath, 1, endPos)

    IfInString, filepath, *
        StringTrimLeft, filepath, filepath, 1

    If FileExist(filepath) {
        cmd = explorer.exe /select,"%filepath%"
        Run, %cmd%
        tt("exploring to: '" filepath "'...", 1)
    }
    Else
        tt("does not exist: '" filepath "'", 2)
}