#Requires AutoHotkey v2.0
#Include <windows>

class WindowsTests {
    class Version {
        returns_string_with_dot() {
            v := windows_get_version()
            if !InStr(v, ".")
                throw Error("Version should contain a dot, got '" v "'")
        }

        major_is_numeric() {
            v := windows_get_version()
            parts := StrSplit(v, ".")
            if !IsInteger(parts[1])
                throw Error("Major version should be numeric, got '" parts[1] "'")
        }

        minor_is_numeric() {
            v := windows_get_version()
            parts := StrSplit(v, ".")
            if !IsInteger(parts[2])
                throw Error("Minor version should be numeric, got '" parts[2] "'")
        }

        major_is_at_least_10() {
            v := windows_get_version()
            parts := StrSplit(v, ".")
            if Integer(parts[1]) < 10
                throw Error("Major version should be >= 10 on modern Windows, got '" parts[1] "'")
        }
    }
}
