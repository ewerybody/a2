#Requires AutoHotkey v2.0
#Include <jxon>

global test_directory_path
SplitPath(A_LineFile, , &test_directory_path)

class JxonTests {
    read_file() {
        test_json_path := A_ScriptFullPath ".json"
        if FileExist(test_json_path)
            FileDelete(test_json_path)

        try {
            Jxon_Read(test_json_path)
        } catch OSError {
        } else {
            throw Error("Jxon_Read should throw OSError on inexistent file!")
        }

        f := FileOpen(test_json_path, 'w')
        test_string := "Hello, World!"
        f.Write('"' test_string '"')
        f.Close()

        data := Jxon_Read(test_json_path)
        if data != test_string
            throw Error("test_string does not match read string!")
    }

    write_array() {
        test_list := ["muppets", 1337, 42, 23, false, "", "😘"]
        test_string := Jxon_Dump(test_list)
        result := Jxon_Load(&test_string)
        if Type(result) != "Array"
            throw Error("result is not of Type Array! (" Type(result) ")")
        For item in result {
            if item != result[A_Index]
                throw Error("Item mismatch! Expected: '" item "' got '" result[A_Index] "'!")
        }
    }
}
