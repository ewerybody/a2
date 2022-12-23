
string_join(array_of_strings, separator:=", ") {
    ; Assemble a single string from a given array of strings.
    result := ""
    Loop(array_of_strings.Length - 1) {
        this_item := array_of_strings[A_Index]
        result .= this_item . separator
    }
    last_item := array_of_strings[array_of_strings.Length]
    result .= last_item
    Return result
}

; Look for string in array. Return index of string if found, Return 0 otherwise.
string_is_in_array(search, array, start := 1) {
    Loop(array.Length) {
        idx := A_Index + start - 1
        if (idx > array.Length)
            Return 0
        if (search = array[idx])
            Return idx
    }
    Return 0
}

string_is_web_address(string) {
    ; Return true if given string looks like an URL
    static WEB_TLDS := ["html", "com", "de", "net", "org", "co.uk"]
    if ( RegExMatch(string, "i)^http://") OR RegExMatch(string, "i)^https://") )
        return true
    else {
        Loop(WEB_TLDS.Length) {
            ext := WEB_TLDS[A_Index]
            sub := SubStr(string, - StrLen(ext))
            if (sub = "." ext)
                return true
        }
    }
}

string_startswith(string, startstr) {
    ; Determine if a string starts with another string.
    ; NOTE: It's a bit faster to simply use InStr(string, startstr) = 1
    return InStr(string, startstr) = 1
}

string_endswith(string, end) {
    ; Determine if a string ends with another string
    return StrLen(end) <= StrLen(string) && Substr(string, -StrLen(end)) = end
}

string_is_whitespace(string) {
    if (string = A_Space OR string = A_Tab OR string = "`n" OR string = "`r")
        return true
    else
        return false
}

; Trim one or more characters from a string start and end.
string_trim(string, chars) {
    return string_trimLeft(string_trimRight(string, chars), chars)
}

string_trimLeft(string, chars) {
    ; Remove all occurences of trim at the beginning of string
    ; trim can be an array of strings that should be removed.
    if (IsObject(chars))
        chars := string_join(chars, "")

    Loop(StrLen(string)) {
        If InStr(chars, SubStr(string, 1, 1))
        {
            string := SubStr(string, 2)
            Continue
        }
        return string
    }
}

string_trimRight(string, chars) {
    ; Remove all occurences of chars at the end of string
    ; chars can be an array of strings that should be removed.
    if (IsObject(chars))
        chars := string_join(chars, "")

    slen := StrLen(string)
    Loop(slen) {
        sub := SubStr(string, -1)
        If InStr(chars, sub)
        {
            string := SubStr(string, 1, slen - A_Index)
            Continue
        }
        return string
    }
}

string_strip(string) {
    ; strip whitespace from start and end of a string:
    ; if first char is space, tab or linefeed, remove it and look again:
    c := SubStr(string, 1, 1)
    if (c = A_Space OR c = A_Tab OR c = "`n" OR c = "`r")
    {
        string := LTrim(string, 1)
        string := string_strip(string)
    }
    ; now last character:
    c := SubStr(string, -1)
    if (c = A_Space OR c = A_Tab OR c = "`n" OR c = "`r")
    {
        string := SubStr(string, 1, -1)
        string := string_strip(string)
    }

    return string
}

string_unquote(string, quote := '"') {
    ; Remove quotes from a string if necessary.
    if (InStr(string, quote) = 1 && string_endsWith(string, quote))
        string := string_trim(string, quote)
    return string
}

string_quote(string, once := 1, quote := '"') {
    ; Add quotes to a string only if necessary.
    if (once) {
        if (InStr(string, quote) != 1)
            string := quote string
        if (!string_endsWith(string, quote))
            string := string quote
        return string
    }
    return quote string quote
}

string_suffix(string, suffix) {
    ; Ensure a string to end with a suffix string.
    if !string_endswith(string, suffix)
        return string suffix
    return string
}

string_prefix(string, prefix) {
    ; Ensure a string to start with a suffix string.
    if !string_startswith(string, prefix)
        return prefix string
    return string
}

; Make back for front flipped version of given string
string_reverse(string) {
    new_string := ""
    Loop(StrLen(string))
        new_string := SubStr(string, A_Index, 1) new_string
    Return new_string
}

; Make string of random UPPER case letters with given length.
string_random(length) {
    txt := ""
    offset := 64
    Loop(length) {
        i := Random(1, 26)
        txt .= Chr(i + offset)
    }
    return txt
}
