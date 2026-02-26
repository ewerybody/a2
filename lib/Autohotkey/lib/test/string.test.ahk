#Requires AutoHotkey v2.0
#Include <string>

class StringTests {
    class Join {
        with_separator() {
            arr := ["a", "b", "c"]
            result := string_join(arr, "||")
            parts := StrSplit(result, "||")
            if (parts.Length != 3)
                throw Error("Expected 3 parts, got " parts.Length)
            Loop(arr.Length) {
                if (parts[A_Index] != arr[A_Index])
                    throw Error("Part " A_Index " mismatch: '" parts[A_Index] "' != '" arr[A_Index] "'")
            }
        }

        empty_separator() {
            result := string_join(["a", "b", "c"], "")
            if (result != "abc")
                throw Error("Expected 'abc', got '" result "'")
        }

        empty_array() {
            result := string_join([], ", ")
            if (result != "")
                throw Error("Empty array should return empty string, got '" result "'")
        }

        preserves_empty_items() {
            expect := "a||||c"
            result := string_join(["a", "", "c"], "||")
            if (result != expect)
                throw Error("Expected '" expect "', got '" result "'")
        }
    }

    class StartsWith {
        matches_case_insensitive() {
            if (!string_startswith("a#$ Bumble-buts", "A#$ "))
                throw Error("Should match start case-insensitively")
        }

        no_match() {
            if (string_startswith(" 3456 Bumble-buts", " 3457 "))
                throw Error("Should not match differing start")
        }
    }

    class EndsWith {
        matches_case_insensitive() {
            if (!string_endswith("NBumble-buts$#%S", "$#%s"))
                throw Error("Should match end case-insensitively")
        }

        no_match() {
            if (string_endswith("NBumble-buts$#%", "9fh3"))
                throw Error("Should not match differing end")
        }
    }

    class Quote {
        round_trip_single_quote() {
            s := "'XKermitX'"
            un := string_unquote(s, "'")
            q := string_quote(un,, quote := "'")
            if (s != q)
                throw Error("Round-trip quote failed: '" s "' != '" q "'")
        }

        unquote_removes_quotes() {
            un := string_unquote("'XFiddlesticksX'", "'")
            if (!string_startswith(un, "X"))
                throw Error("Unquoted string should start with X, got '" un "'")
            if (!string_endswith(un, "X"))
                throw Error("Unquoted string should end with X, got '" un "'")
        }

        unquote_unquoted_is_noop() {
            p := A_ScriptFullPath
            if (p != string_unquote(p))
                throw Error("Unquoting an already-unquoted string should be a noop")
        }

        quote_once_no_duplicate() {
            s := "'XAutohotkeyX'"
            un := string_unquote(s, "'")
            q := string_quote(un, once := 1, quote := "'")
            if (s != q)
                throw Error("Quote once failed: '" s "' != '" q "'")
        }
    }

    class IsInArray {
        found() {
            if (!string_is_in_array("b", ["a", "b", "c"]))
                throw Error("'b' should be found in array")
        }

        case_sensitive_not_found() {
            if (string_is_in_array("B", ["a", "b", "c"]))
                throw Error("'B' should not match 'b' (case-sensitive)")
        }

        start_offset_skips_earlier() {
            if (string_is_in_array("a", ["a", "b", "c"], 2))
                throw Error("'a' at index 1 should not be found when starting at index 2")
        }

        returns_correct_index() {
            idx := string_is_in_array("c", ["a", "b", "c"])
            if (idx != 3)
                throw Error("'c' should be at index 3, got " idx)
        }
    }

    class Suffix {
        suffix_is_added() {
            result := string_suffix("Free Assange", "!")
            if (result != "Free Assange!")
                throw Error("Suffix should be added, got '" result "'")
        }

        suffix_not_duplicated() {
            result := string_suffix("Free Assange!", "!")
            if (result != "Free Assange!")
                throw Error("Suffix should not be duplicated, got '" result "'")
        }
    }

    class Prefix {
        prefix_noop_when_present() {
            st := "Free Assange"
            result := string_prefix(st, "Free")
            if (result != st)
                throw Error("Prefix already present, should be noop, got '" result "'")
        }

        prefix_is_added() {
            result := string_prefix("Assange", "Free ")
            if (result != "Free Assange")
                throw Error("Prefix should be added, got '" result "'")
        }
    }

    class Reverse {
        double_reverse_is_identity() {
            st := "Test Reverse"
            if (st != string_reverse(string_reverse(st)))
                throw Error("Double reverse should equal original")
        }

        reverses_correctly() {
            result := string_reverse("abc")
            if (result != "cba")
                throw Error("'abc' reversed should be 'cba', got '" result "'")
        }
    }

    class Random {
        correct_length() {
            result := string_random(32)
            if (StrLen(result) != 32)
                throw Error("Expected length 32, got " StrLen(result))
        }

        uppercase_letters_only() {
            result := string_random(20)
            if (!RegExMatch(result, "^[A-Z]+$"))
                throw Error("Expected only uppercase A-Z letters, got '" result "'")
        }
    }

    class Strip {
        strip_chars_both_ends() {
            result := string_strip('abc "><"abc ', ' "abc')
            if (result != "><")
                throw Error("Expected '><', got '" result "'")
        }

        strips_left() {
            result := string_strip_left("xxx" "hello", "x")
            if (result != "hello")
                throw Error("Expected 'hello', got '" result "'")
        }

        strips_right() {
            result := string_strip_right("hello" "yyy", "y")
            if (result != "hello")
                throw Error("Expected 'hello', got '" result "'!")
        }

        strips_trailing_whitespace() {
            st := "hello, world!"
            result := string_strip(st " `n")
            if (result != st)
                throw Error("Expected '" st "', got '" result "'!")
        }

        strips_leading_whitespace() {
            expect := "hello"
            result := string_strip("  `n" expect)
            if (result != "hello")
                throw Error("Expected '" expect "', got '" result "'!")
        }
    }

    class IsWebAddress {
        http_url() {
            if (!string_is_web_address("http://example.com"))
                throw Error("http:// URL should be a web address")
        }

        https_url() {
            if (!string_is_web_address("https://example.com"))
                throw Error("https:// URL should be a web address")
        }

        dot_com_domain() {
            if (!string_is_web_address("example.com"))
                throw Error(".com domain should be a web address")
        }

        plain_string_is_not() {
            if (string_is_web_address("just a string"))
                throw Error("Plain string should not be a web address")
        }
    }
}
