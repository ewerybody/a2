
; Assemble a single string from a given array of strings.
string_join(array_of_strings, separator:=", ", default:="") {
    result := ""
    if not array_of_strings.Length
        Return result

    Loop(array_of_strings.Length - 1)
        result .= array_of_strings.get(A_Index, default) . separator
    last_item := array_of_strings.get(array_of_strings.Length, default)
    result .= last_item
    Return result
}

; Tell if a search string is in an array object of strings.
string_is_in_array(search, string_list, start := 1) {
    ; returns index of search string if found
    ; returns 0 otherwise
    Loop(string_list.Length) {
        idx := A_Index + start - 1
        if idx > string_list.Length
            Return 0
        if (search == string_list[idx])
            Return idx
    }
    Return 0
}

; Return true if given string looks like an URL.
string_is_web_address(string) {
    if ( RegExMatch(string, "i)^http://") OR RegExMatch(string, "i)^https://") )
        return true

    web_suffixes := ["html", "com", "de", "net", "org", "co.uk"]
    Loop(web_suffixes.Length) {
        ext := "." . web_suffixes[A_Index]
        sub := SubStr(string, - StrLen(ext))
        if (sub == ext)
            return true
    }
    return false
}

; Determine if a string starts with another string.
string_startswith(string, start_str) {
    ; NOTE: It's a bit faster to simply use InStr(string, start_str) = 1
    return InStr(string, start_str) = 1
}

; Determine if a string ends with another string
string_endswith(string, end) {
    return StrLen(end) <= StrLen(string) && Substr(string, -StrLen(end)) = end
}

; Strip or trim whitespace from start and end of a string.
string_strip(string, omit_chars := "") {
    if omit_chars == ""
        omit_chars := " `t`n`r"
    return Trim(string, omit_chars)
}

string_strip_right(string, omit_chars := "") {
    if omit_chars == ""
        omit_chars := " `t`n`r"
    return RTrim(string, omit_chars)
}

string_strip_left(string, omit_chars := "") {
    if omit_chars == ""
        omit_chars := " `t`n`r"
    return LTrim(string, omit_chars)
}

; Remove quotes from a string if necessary.
string_unquote(string, quote := '"') {
    if (InStr(string, quote) = 1 && string_endsWith(string, quote))
        string := string_strip(string, quote)
    return string
}

; Add quotes to a string only if necessary.
string_quote(string, once := 1, quote := '"') {
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
    Loop(length)
    {
        i := Random(1, 26)
        txt .= Chr(i + offset)
    }
    return txt
}
