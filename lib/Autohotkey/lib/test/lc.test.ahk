#Requires AutoHotkey v2.0
#Include <LC>

class LcTests {
    class Base64ToBuf {
        decodes_simple_string() {
            ; "aGVsbG8=" is base64 for "hello" (ASCII: 104 101 108 108 111)
            n := LC_Base64ToBuf("aGVsbG8=", &buf)
            if n != 5
                throw Error("Expected 5 bytes, got " n)
            expected := [104, 101, 108, 108, 111]
            loop expected.Length {
                b := NumGet(buf, A_Index - 1, "UChar")
                if b != expected[A_Index]
                    throw Error("Byte " A_Index ": expected " expected[A_Index] ", got " b)
            }
        }

        strips_data_uri_prefix() {
            n := LC_Base64ToBuf("data:image/png;base64,aGVsbG8=", &buf)
            if n != 5
                throw Error("Expected 5 bytes after stripping data-URI prefix, got " n)
        }

        strips_whitespace_and_newlines() {
            ; split base64 with spaces/newlines — should still decode
            n := LC_Base64ToBuf("aGVs`nbG8=", &buf)
            if n != 5
                throw Error("Expected 5 bytes after stripping whitespace, got " n)
        }

        throws_on_empty_string() {
            threw := false
            try {
                LC_Base64ToBuf("", &buf)
            } catch Error {
                threw := true
            }
            if !threw
                throw Error("Expected an error for empty base64 string")
        }
    }
}
