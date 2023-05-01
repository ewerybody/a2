#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

; Move a file or directory, tell true/false 1/0 if it worked.
secure_move(from_path, to_path) {
    attrs := FileExist(from_path)
    if (attrs == ""):
        return false

    if (InStr(attrs, "D")) {
        FileMoveDir, %from_path%, %to_path%
    } else {
        FileMove, %from_path%, %to_path%
    }
    If ErrorLEvel
        MsgBox ErrorLEvel: %ErrorLEvel%

    if (!FileExist(from_path) AND FileExist(to_path))
        return true
    else
        return false
}

