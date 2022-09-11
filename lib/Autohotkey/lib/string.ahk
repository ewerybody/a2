
string_join(byref array_of_strings, byref separator=", ") {
    ; Assemble a single string from a given array of strings.
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

string_is_in_array(byref search, byref array, start := 1) {
    ; look up the items of an array object
    ; returns index of search string if found
    ; returns 0 otherwise
    Loop % array.MaxIndex() {
        idx := A_Index + start - 1
        if (search == array[idx])
            Return idx
    }
    Return 0
}

string_is_web_address(string) {
    ; Return true if given string looks like an URL
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

string_startswith(byref string, byref startstr) {
    ; Determine if a string starts with another string.
    ; NOTE: It's a bit faster to simply use InStr(string, startstr) = 1
    return InStr(string, startstr) = 1
}

string_endswith(byref string, byref end) {
    ; Determine if a string ends with another string
    return strlen(end) <= strlen(string) && Substr(string, -strlen(end) + 1) = end
}

is_whitespace(byref string) {
    if (string == A_Space OR string == A_Tab OR string == "`n" OR string == "`r")
        return true
    else
        return false
}

string_trim(byref string, byref chars) {
    return string_trimLeft(string_trimRight(string, chars), chars)
}

string_trimLeft(string, chars) {
    ; Remove all occurences of trim at the beginning of string
    ; trim can be an array of strings that should be removed.
    if (!IsObject(chars))
        chars := [chars]
    for index, trimString in chars
    {
        len := StrLen(trimString)
        while(SubStr(String, 1, len) == trimString)
            string := SubStr(String, len + 1)
    }
    return string
}

string_trimRight(string, chars) {
    ; Remove all occurences of trim at the end of string
    ; trim can be an array of strings that should be removed.
    if (!IsObject(chars))
        chars := [chars]
    for index, trimString in chars
    {
        len := strLen(trimString)
        while(string_endsWith(string, trimString))
            StringTrimRight, string, string, %len%
    }
    return string
}

string_strip(string) {
    ; strip whitespace from start and end of a string:
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

string_unquote(string, quote = """") {
    ; Remove quotes from a string if necessary.
    if (InStr(string, quote) = 1 && string_endsWith(string, quote))
        string := string_trim(string, quote)
    return string
}

string_quote(string, once = 1, quote = """") {
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

string_reverse(byref string) {
    new_string := ""
    Loop, % StrLen(string)
        new_string := SubStr(string, A_Index, 1) new_string
    Return new_string
}
