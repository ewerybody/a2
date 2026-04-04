;a2 Autohotkey path library.
#include <string>

/**
 * Check if a path is absolute or relative.
 * @param {(String)} path
 * Path to check.
 * @returns {(Boolean)}
 * True if absolute, false if relative.
 */
path_is_absolute(path) {
    SplitPath path ,,,,, &OutDrive
    return OutDrive != ""
}

/**
 * Return the parent directory of a path.
 * @param {(String)} path
 * Path to get the parent of.
 * @param {(Integer)} [n_parent]
 * Number of times to get parent directory name. Default: 1
 * @returns {(String)}
 * Parent directory path.
 */
path_dirname(path, n_parent := 1) {
    if (n_parent <= 1) {
        SplitPath path,, &out_dir
        return out_dir
    }
    out_dir := path
    Loop(n_parent)
        SplitPath out_dir,, &out_dir
    return out_dir
}

/**
 * Return the filename portion of a path, without its directory.
 * @param {(String)} path
 * Path to get the filename from.
 * @returns {(String)}
 * Filename with extension.
 */
path_basename(path) {
    SplitPath path, &OutFileName
    return OutFileName
}

/**
 * Split a path into its base name and extension.
 * @param {(String)} path
 * Path to split.
 * @returns {(Array)}
 * Two-element array: [name_without_extension, extension].
 */
path_split_ext(path) {
    SplitPath path,,, &OutExtension, &OutNameNoExt
    return [OutNameNoExt, OutExtension]
}

/**
 * Check if a path exists and is a directory.
 * @param {(String)} path
 * Path to check.
 * @returns {(Boolean)}
 * True if path is an existing directory.
 */
path_is_dir(path) {
    return InStr(FileExist(path), "D") > 0
}

/**
 * Check if a path exists and is a file.
 * @param {(String)} path
 * Path to check.
 * @returns {(Boolean)}
 * True if path is an existing file.
 */
path_is_file(path) {
    attrs := FileExist(path)
    return attrs != "" && !InStr(attrs, "D")
}

/**
 * Join path parts, handling extra or missing backslashes.
 * @param {(String)} base_path
 * Base path to join onto.
 * @param {(String)} items*
 * One or more path parts to append.
 * @returns {(String)}
 * Joined path string.
 */
path_join(base_path, items*) {
    path := RTrim(base_path, "\")
    Loop(items.Length)
        path .= "\" Trim(items[A_Index], "\")
    return path
}

/**
 * Resolve a path, expanding `.` and `..` components.
 * @param {(String)} path
 * Path to normalize.
 * @returns {(String)}
 * Absolute normalized path.
 */
path_normalize(path) {
    ; From the documentation - https://www.autohotkey.com/docs/misc/LongPaths.htm
    cc := DllCall("GetFullPathName", "str", path, "uint", 0, "ptr", 0, "ptr", 0, "uint")
    VarSetStrCapacity(&buf, cc*2)
    DllCall("GetFullPathName", "str", path, "uint", cc, "str", buf, "ptr", 0)
    return buf
}

/**
 * Check if a directory contains no files or subdirectories.
 * @param {(String)} path
 * Directory path to check.
 * @returns {(Boolean)}
 * True if the directory is empty.
 */
path_is_empty(path) {
    Loop Files, path "\*", "FD"
        return false
    return true
}

/**
 * Check if a path is writable (not read-only).
 * @param {(String)} path
 * Path to check.
 * @returns {(Boolean)}
 * True if the path is writable.
 */
path_is_writeable(path) {
    if InStr(FileGetAttrib(path), "R")
        return false
    return true
}

/**
 * Remove the read-only attribute from a path.
 * @param {(String)} path
 * Path to make writable.
 */
path_set_writable(path) {
    FileSetAttrib("-R", path)
}

/**
 * Set the read-only attribute on a path.
 * @param {(String)} path
 * Path to make read-only.
 */
path_set_readonly(path) {
    FileSetAttrib("+R", path)
}

/**
 * Expand %environment_variable% references in a path.
 * Handles multiple variables in a single path string.
 * @param {(String)} path
 * Path string potentially containing %VAR% references.
 * @returns {(String)}
 * Path with all known environment variables expanded.
 */
path_expand_env(path) {
    while InStr(path, "%") {
        pos1 := InStr(path, "%")
        pos2 := InStr(path, "%",, pos1 + 1)
        if !pos2
            break
        subs := SubStr(path, pos1 + 1, pos2 - pos1 - 1)
        env_val := EnvGet(subs)
        if (env_val == "")
            break
        path := StrReplace(path, "%" subs "%", env_val)
    }
    return path
}

/**
 * Return the path to a file neighboring another file in the same directory.
 * Handy with the builtin var `A_LineFile`.
 * @param {(String)} file_path
 * Reference file path.
 * @param {(String)} neighbor_name
 * Name of the neighboring file.
 * @returns {(String)}
 * Full path to the neighbor.
 */
path_neighbor(file_path, neighbor_name) {
    return path_join(path_dirname(file_path), neighbor_name)
}

/**
 * Get next free file name. If already existing add numbers to
 * file name until a free one is found.
 * @param {(String)} dir_path
 * Directory to look for names.
 * @param {(String)} file_name
 * Initial file name to iterate on.
 * @param {(String)} ext
 * File extension.
 * @param {(String)} [separator]
 * Separator to put between file name and numbers.
 * @returns {(String)}
 * A file name (without directory or extension) that does not exist in dir_path.
 */
path_get_free_name(dir_path, file_name, ext, separator := "") {
    if !file_name AND !ext
        return file_name

    ext := string_prefix(Trim(ext), ".")
    file_path := path_join(dir_path, file_name . ext)
    if !FileExist(file_path)
        return file_name

    index := 1
    Loop {
        base := file_name . separator . index
        file_path := path_join(dir_path, base . ext)
        if !FileExist(file_path)
            return base
        index++
    }
}

/**
 * Get list of files in given `dir_path` with a single call.
 * @param {(String)} dir_path
 * Directory to look for files.
 * @param {(String)} [pattern]
 * Pattern to filter for. Default: "*" for any files.
 * @param {(String)} [full_path]
 * Set true to get list of full paths. Default: false.
 * @returns {(Array)}
 * Array with string file names or paths.
 */
path_get_files(dir_path, pattern := "*", full_path := false) {
    files := []
    Loop Files dir_path "\" pattern, "F" {
        if full_path
            files.Push(A_LoopFileFullPath)
        else
            files.Push(A_LoopFileName)
    }
    return files
}
