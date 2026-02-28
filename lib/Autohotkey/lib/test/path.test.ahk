#Requires AutoHotkey v2.0
#Include <path>

class PathTests {
    class IsAbsolute {
        relative_is_not_absolute() {
            if path_is_absolute("\..\some\relative")
                throw Error("Relative path should not be absolute")
        }

        script_path_is_absolute() {
            if !path_is_absolute(A_ScriptFullPath)
                throw Error("A_ScriptFullPath should be absolute")
        }

        normalized_path_is_absolute() {
            p := path_normalize(A_ScriptDir . "\..\..\whatever")
            if !path_is_absolute(p)
                throw Error("Normalized path should be absolute, got '" p "'")
        }
    }

    class Dirname {
        returns_parent_dir() {
            result := path_dirname(A_ScriptFullPath)
            if result != A_ScriptDir
                throw Error("Expected '" A_ScriptDir "', got '" result "'")
        }

        double_dirname_goes_up() {
            expected := path_dirname(A_ScriptDir)
            result := path_dirname(path_dirname(A_ScriptFullPath))
            if result != expected
                throw Error("Expected '" expected "', got '" result "'")
        }
    }

    class Basename {
        returns_filename() {
            result := path_basename(A_ScriptFullPath)
            if result != A_ScriptName
                throw Error("Expected '" A_ScriptName "', got '" result "'")
        }
    }

    class SplitExt {
        splits_name_and_ext() {
            parts := path_split_ext("C:\foo\bar.txt")
            if parts[1] != "bar"
                throw Error("Expected name 'bar', got '" parts[1] "'")
            if parts[2] != "txt"
                throw Error("Expected ext 'txt', got '" parts[2] "'")
        }

        script_has_ahk_extension() {
            parts := path_split_ext(A_ScriptFullPath)
            if parts[2] != "ahk"
                throw Error("Expected extension 'ahk', got '" parts[2] "'")
        }
    }

    class Join {
        joins_multiple_parts() {
            result := path_join("C:\foo", "bar", "baz.txt")
            if result != "C:\foo\bar\baz.txt"
                throw Error("Expected 'C:\\foo\\bar\\baz.txt', got '" result "'")
        }

        strips_extra_slashes() {
            result := path_join("C:\foo\", "\bar.txt")
            if result != "C:\foo\bar.txt"
                throw Error("Expected 'C:\\foo\\bar.txt', got '" result "'")
        }

        roundtrip_with_dirname_and_basename() {
            result := path_join(path_dirname(A_ScriptFullPath), path_basename(A_ScriptFullPath))
            if result != A_ScriptFullPath
                throw Error("Expected '" A_ScriptFullPath "', got '" result "'")
        }
    }

    class Normalize {
        resolves_dotdot() {
            p := path_normalize(A_ScriptDir . "\..\..\ASD")
            if InStr(p, "..")
                throw Error("Normalized path should not contain '..', got '" p "'")
        }

        result_is_absolute() {
            p := path_normalize(A_ScriptDir . "\..\..\ASD")
            if !path_is_absolute(p)
                throw Error("Normalized path should be absolute, got '" p "'")
        }
    }

    class IsDir {
        script_dir_is_dir() {
            if !path_is_dir(A_ScriptDir)
                throw Error("A_ScriptDir should be a directory")
        }

        script_file_is_not_dir() {
            if path_is_dir(A_ScriptFullPath)
                throw Error("Script file should not be a directory")
        }

        nonexistent_is_not_dir() {
            if path_is_dir(A_ScriptDir . "\_nonexistent_xyz_")
                throw Error("Nonexistent path should not be a directory")
        }
    }

    class IsFile {
        script_is_file() {
            if !path_is_file(A_ScriptFullPath)
                throw Error("Script path should be a file")
        }

        dir_is_not_file() {
            if path_is_file(A_ScriptDir)
                throw Error("Directory should not be a file")
        }

        nonexistent_is_not_file() {
            if path_is_file(A_ScriptDir . "\_nonexistent_xyz_.txt")
                throw Error("Nonexistent path should not be a file")
        }
    }

    class IsEmpty {
        script_dir_is_not_empty() {
            if path_is_empty(A_ScriptDir)
                throw Error("Script dir should not be empty")
        }

        fresh_dir_is_empty() {
            test_dir := A_ScriptDir . "\_ emptytest_path_8f3kq"
            DirCreate(test_dir)
            try {
                if !path_is_empty(test_dir)
                    throw Error("Freshly created dir should be empty")
            } finally {
                DirDelete(test_dir)
            }
        }
    }

    class Writeable {
        set_readonly_then_writable() {
            test_file := path_join(A_ScriptDir, "_write_test_path_tmp")
            FileAppend("", test_file)
            try {
                path_set_readonly(test_file)
                if path_is_writeable(test_file)
                    throw Error("File should be read-only after path_set_readonly")
                path_set_writable(test_file)
                if !path_is_writeable(test_file)
                    throw Error("File should be writable after path_set_writable")
            } finally {
                path_set_writable(test_file)
                FileDelete(test_file)
            }
        }
    }

    class ExpandEnv {
        expands_system_root() {
            result := path_expand_env("%SystemRoot%\System32\imageres.dll")
            if InStr(result, "%")
                throw Error("Expanded path should not contain '%', got '" result "'")
        }

        expanded_path_exists() {
            result := path_expand_env("%SystemRoot%\System32\imageres.dll")
            if !FileExist(result)
                throw Error("Expanded path should exist: '" result "'")
        }

        expands_multiple_vars() {
            result := path_expand_env("%HOMEDRIVE%%HOMEPATH%")
            if InStr(result, "%")
                throw Error("Multiple vars should all be expanded, got '" result "'")
            if !path_is_dir(result)
                throw Error("Expanded %HOMEDRIVE%%HOMEPATH% should be an existing dir, got '" result "'")
        }

        no_var_is_noop() {
            p := "C:\no\env\var\here.txt"
            result := path_expand_env(p)
            if result != p
                throw Error("Path without env vars should be unchanged, got '" result "'")
        }
    }

    class Neighbor {
        returns_sibling_path() {
            expected := path_join(A_ScriptDir, "other.ahk")
            result := path_neighbor(A_ScriptFullPath, "other.ahk")
            if result != expected
                throw Error("Expected '" expected "', got '" result "'")
        }
    }

    class GetFreeName {
        no_conflict_returns_original() {
            result := path_get_free_name(A_ScriptDir, "_pth_noexist_xyzfree_", "txt")
            if result != "_pth_noexist_xyzfree_"
                throw Error("Expected original name, got '" result "'")
        }

        conflict_returns_incremented() {
            base := "_test_pth_free"
            FileAppend("", A_ScriptDir . "\" base ".txt")
            Loop(3)
                FileAppend("", A_ScriptDir . "\" base A_Index ".txt")
            try {
                result := path_get_free_name(A_ScriptDir, base, "txt")
                if result != base "4"
                    throw Error("Expected '" base "4', got '" result "'")
            } finally {
                FileDelete(A_ScriptDir . "\" base ".txt")
                Loop(3)
                    FileDelete(A_ScriptDir . "\" base A_Index ".txt")
            }
        }

        starts_from_one() {
            base := "_test_pth_start"
            FileAppend("", A_ScriptDir . "\" base ".txt")
            try {
                result := path_get_free_name(A_ScriptDir, base, "txt")
                if result != base "1"
                    throw Error("Expected '" base "1', got '" result "'")
            } finally {
                FileDelete(A_ScriptDir . "\" base ".txt")
            }
        }

        separator_is_respected() {
            base := "_test_pth_sep"
            FileAppend("", A_ScriptDir . "\" base ".txt")
            try {
                result := path_get_free_name(A_ScriptDir, base, "txt", "__")
                if result != base "__1"
                    throw Error("Expected '" base "__1', got '" result "'")
            } finally {
                FileDelete(A_ScriptDir . "\" base ".txt")
            }
        }

        empty_name_returns_falsy() {
            result := path_get_free_name(A_ScriptDir, "", "")
            if result
                throw Error("Empty name/ext should return falsy, got '" result "'")
        }
    }
}
