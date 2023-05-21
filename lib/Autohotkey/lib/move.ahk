#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

; Move a file or directory, tell true/false 1/0 if it worked.
move_secure(from_path, to_path) {
    attrs := FileExist(from_path)
    if (attrs == "")
        return false

    if (InStr(attrs, "D")) {
        FileMoveDir, %from_path%, %to_path%
    } else {
        FileMove, %from_path%, %to_path%
    }
    ; If ErrorLEvel
    ;     MsgBox ErrorLEvel: %ErrorLEvel% %from_path%

    if (!FileExist(from_path) AND FileExist(to_path))
        return true
    else
        return false
}

; Try moving a list of items. Rollback everything if it breaks.
move_catched(source_dir, target_dir, relative_paths) {
    done_items := []
    for i, rel_path in relative_paths
    {
        source := path_join(source_dir, rel_path)
        target := path_join(target_dir, rel_path)
        if move_secure(source, target)
            done_items.Push(rel_path)
        else
        {
            ; msgbox_error("Could not move " rel_path " from/to:`n" source_dir "`n" target_dir)
            rollback_result := move_catched(target_dir, source_dir, done_items)
            ; MsgBox rollback_result: %rollback_result%
            return false
        }
    }
    return true
}
