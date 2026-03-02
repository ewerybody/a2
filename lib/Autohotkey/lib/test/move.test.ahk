#Requires AutoHotkey v2.0
#Include <move>
#Include <path>

_move_test_dir(suffix) {
    test_dir := path_join(A_Temp, "_a2_move_test_" suffix)
    if FileExist(test_dir)
        DirDelete(test_dir, 1)
    DirCreate(test_dir)
    return test_dir
}

_move_list_dir(dir_path) {
    items := []
    Loop Files dir_path . "\*", "FD"
        items.Push(A_LoopFileName)
    return items
}

class MoveTests {
    class Secure {
        simple_dir_move() {
            src := _move_test_dir("secure_a")
            dst := src . "_dst"
            try {
                result := move_secure(src, dst)
                if !result
                    throw Error("move_secure should return true for valid dir move")
                if FileExist(src)
                    throw Error("Source should not exist after move")
                if !FileExist(dst)
                    throw Error("Destination should exist after move")
            } finally {
                if FileExist(src)
                    DirDelete(src, 1)
                if FileExist(dst)
                    DirDelete(dst, 1)
            }
        }

        fails_when_target_exists() {
            src := _move_test_dir("secure_b")
            dst := src . "_dst"
            DirCreate(dst)
            try {
                result := move_secure(src, dst)
                if result
                    throw Error("move_secure should return false when target already exists")
            } finally {
                if FileExist(src)
                    DirDelete(src, 1)
                if FileExist(dst)
                    DirDelete(dst, 1)
            }
        }

        returns_false_for_missing_source() {
            result := move_secure(A_Temp . "\_a2_no_exist_src_xyz_", A_Temp . "\_a2_no_exist_dst_xyz_")
            if result
                throw Error("move_secure should return false for nonexistent source")
        }

        file_move() {
            src := path_join(A_Temp, "_a2_move_test_file_src.txt")
            dst := path_join(A_Temp, "_a2_move_test_file_dst.txt")
            FileAppend("test content", src)
            try {
                result := move_secure(src, dst)
                if !result
                    throw Error("move_secure should return true for file move")
                if FileExist(src)
                    throw Error("Source file should not exist after move")
                if !FileExist(dst)
                    throw Error("Destination file should exist after move")
            } finally {
                if FileExist(src)
                    FileDelete(src)
                if FileExist(dst)
                    FileDelete(dst)
            }
        }
    }

    class Atomic {
        empty_list_succeeds() {
            src := _move_test_dir("atomic_empty_src")
            dst := _move_test_dir("atomic_empty_dst")
            try {
                result := move_atomic(src, dst, [])
                if result != ""
                    throw Error("move_atomic with empty list should succeed, got '" result "'")
            } finally {
                if FileExist(src)
                    DirDelete(src, 1)
                if FileExist(dst)
                    DirDelete(dst, 1)
            }
        }

        moves_files_to_target() {
            src := _move_test_dir("atomic_files_src")
            dst := _move_test_dir("atomic_files_dst")
            FileAppend("a", path_join(src, "file_a.txt"))
            FileAppend("b", path_join(src, "file_b.txt"))
            file_list := _move_list_dir(src)
            try {
                result := move_atomic(src, dst, file_list)
                if result != ""
                    throw Error("move_atomic should succeed, got '" result "'")
                if !path_is_empty(src)
                    throw Error("Source should be empty after successful move")
                dst_list := _move_list_dir(dst)
                if dst_list.Length != file_list.Length
                    throw Error("Destination should have all " file_list.Length " moved files, got " dst_list.Length)
            } finally {
                if FileExist(src)
                    DirDelete(src, 1)
                if FileExist(dst)
                    DirDelete(dst, 1)
            }
        }

        rollback_on_conflict() {
            ; Pre-existing file in dst causes the second move to fail, triggering rollback.
            src := _move_test_dir("atomic_conflict_src")
            dst := _move_test_dir("atomic_conflict_dst")
            FileAppend("first", path_join(src, "file1.txt"))
            FileAppend("second", path_join(src, "file2.txt"))
            FileAppend("existing", path_join(dst, "file2.txt"))
            try {
                result := move_atomic(src, dst, ["file1.txt", "file2.txt"])
                if result == ""
                    throw Error("Expected failure due to conflict in dst, got empty string")
                if !FileExist(path_join(src, "file1.txt"))
                    throw Error("file1.txt should be rolled back to source after conflict")
                if !FileExist(path_join(src, "file2.txt"))
                    throw Error("file2.txt should still be in source")
            } finally {
                if FileExist(src)
                    DirDelete(src, 1)
                if FileExist(dst)
                    DirDelete(dst, 1)
            }
        }
    }
}
