/**
 * Move a file or directory safely.
 * @param {(String)} from_path
 * Source path to move from.
 * @param {(String)} to_path
 * Destination path to move to.
 * @returns {(Boolean)}
 * True if the move succeeded, false otherwise.
 */
move_secure(from_path, to_path) {
    attrs := FileExist(from_path)
    if (attrs == "")
        return false

    if (InStr(attrs, "D")) {
        try
            DirMove(from_path, to_path)
        catch
            Return false

    } else {
        try
            FileMove(from_path, to_path)
        catch
            return false
    }

    if (!FileExist(from_path) AND FileExist(to_path))
        return true
    else
        return false
}

/**
 * Atomically move a list of relative paths from source to target directory.
 * If any move fails, all previously completed moves are rolled back.
 * @param {(String)} source_dir
 * Source directory containing the items to move.
 * @param {(String)} target_dir
 * Target directory to move items into.
 * @param {(Array)} relative_paths
 * List of relative file/directory names to move.
 * @returns {(String)}
 * Empty string on full success. On failure, the blocking source and target
 * paths separated by a newline.
 */
move_atomic(source_dir, target_dir, relative_paths) {
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
            rollback_result := move_atomic(target_dir, source_dir, done_items)
            return source "`n" target
        }
    }
    return ""
}
