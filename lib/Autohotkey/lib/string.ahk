﻿
; Assemble a single string from a given array of strings.
string_join(byref array_of_strings, byref separator=", ") {
    result := ""
    Loop, % array_of_strings.MaxIndex() - 1
    {
        this_item := array_of_strings[A_Index]
        result .= this_item . separator
    }
    last_item := array_of_strings[array_of_strings.MaxIndex()]
    result .= last_item
    Return result
}

; Tell if a search string is in an array object of strings.
string_is_in_array(byref search, byref array, start := 1) {
    ; returns index of search string if found
    ; returns 0 otherwise
    Loop % array.MaxIndex() {
        idx := A_Index + start - 1
        if (search == array[idx])
            Return idx
    }
    Return 0
}

; Return true if given string looks like an URL.
string_is_web_address(string) {
    if ( RegExMatch(string, "i)^http://") OR RegExMatch(string, "i)^https://") )
        return true
    else {
        Loop, % WEB_TLDS.MaxIndex() {
            ext := WEB_TLDS[A_Index]
            sub := SubStr(string, - StrLen(ext))
            if (sub == "." ext)
                return true
        }
    }
}

; Determine if a string starts with another string.
string_startswith(byref string, byref startstr) {
    ; NOTE: It's a bit faster to simply use InStr(string, startstr) = 1
    return InStr(string, startstr) = 1
}

; Determine if a string ends with another string
string_endswith(byref string, byref end) {
    return strlen(end) <= strlen(string) && Substr(string, -strlen(end) + 1) = end
}

string_is_whitespace(byref string) {
    if (string == A_Space OR string == A_Tab OR string == "`n" OR string == "`r")
        return true
    else
        return false
}

; Trim one or more characters from a string start and end.
string_trim(byref string, byref chars) {
    return string_trimLeft(string_trimRight(string, chars), chars)
}

; Remove all occurences of chars at beginning of string. chars can be array of strings to be removed.
string_trimLeft(string, chars) {
    if (IsObject(chars))
        chars := string_join(chars, "")

    StringLen, slen, string
    Loop % slen
    {
        If InStr(chars, SubStr(string, 1, 1))
        {
            string := SubStr(string, 2)
            Continue
        }
        return string
    }
}

; Remove all occurences of chars at the end of string. chars can be array of strings to be removed.
string_trimRight(string, chars) {
    if (IsObject(chars))
        chars := string_join(chars, "")

    StringLen, slen, string
    Loop % slen
    {
        If InStr(chars, SubStr(string, 0))
        {
            string := SubStr(string, 1, slen - A_Index)
            Continue
        }
        return string
    }
}

; Strip whitespace from start and end of a string.
string_strip(string) {
    ; if first char is space, tab or linefeed, remove it and look again:
    c := SubStr(string, 1, 1)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimLeft, string, string, 1
        string := string_strip(string)
    }
    ; now last character:
    c := SubStr(string, 0)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimRight, string, string, 1
        string := string_strip(string)
    }

    return string
}

; Remove quotes from a string if necessary.
string_unquote(string, quote = """") {
    if (InStr(string, quote) = 1 && string_endsWith(string, quote))
        string := string_trim(string, quote)
    return string
}

; Add quotes to a string only if necessary.
string_quote(string, once = 1, quote = """") {
    if (once) {
        if (InStr(string, quote) != 1)
            string := quote string
        if (!string_endsWith(string, quote))
            string := string quote
        return string
    }
    return quote string quote
}

; Ensure a string to end with a suffix string.
string_suffix(string, suffix) {
    if !string_endswith(string, suffix)
        return string suffix
    return string
}

; Ensure a string to start with a suffix string.
string_prefix(string, prefix) {
    if !string_startswith(string, prefix)
        return prefix string
    return string
}

; Make back for front flipped version of given string
string_reverse(byref string) {
    new_string := ""
    Loop, % StrLen(string)
        new_string := SubStr(string, A_Index, 1) new_string
    Return new_string
}

; Make string of random UPPER case letters with given length.
string_random(length) {
    txt := ""
    offset := 64
    Loop, %length%
    {
        Random, i , 1, 26
        txt .= Chr(i + offset)
    }
    return txt
}
