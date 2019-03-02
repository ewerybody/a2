; Assembles a single string from a given array of strings.

string_join(byref array_of_strings, byref separator=", ") {
    result := ""
    Loop, % array_of_strings.MaxIndex() - 1
    {
        this_item := array_of_strings[A_Index]
        result = %result%%this_item%%separator%
    }
    last_item := array_of_strings[array_of_strings.MaxIndex()]
    result = %result%%last_item%
    Return, result
}


; looks up the items of an array object
; returns index of search string if found
; returns 0 otherwise
string_is_in_array(byref search, byref array) {
    ;for i, value in array {
    Loop % array.MaxIndex() {
        if (search == array[A_Index])
            Return A_Index
    }
    Return 0
}


; Returns true if given string looks like an URL
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

; Determines if a string starts with another string.
; NOTE: It's a bit faster to simply use InStr(string, startstr) = 1
string_startswith(byref string, byref startstr)
{
    return InStr(string, startstr) = 1
}

; Determines if a string ends with another string
string_endswith(byref string, byref end)
{
    return strlen(end) <= strlen(string) && Substr(string, -strlen(end) + 1) = end
}


is_whitespace(byref string) {
    if (string == A_Space OR string == A_Tab OR string == "`n" OR string == "`r")
        return true
    else
        return false
}


string_trim(byref string, byref trim)
{
    return string_trimLeft(string_trimRight(string, trim), trim)
}

; Removes all occurences of trim at the beginning of string
; trim can be an array of strings that should be removed.
string_trimLeft(string, trim)
{
    if (!IsObject(trim))
        trim := [trim]
    for index, trimString in trim
    {
        len := strLen(trimString)
        while(InStr(string, trimString) = 1)
            StringTrimLeft, string, string, %len%
    }
    return string
}

; Removes all occurences of trim at the end of string
; trim can be an array of strings that should be removed.
string_trimRight(string, trim)
{
    if (!IsObject(trim))
        trim := [trim]
    for index, trimString in trim
    {
        len := strLen(trimString)
        while(string_endsWith(string, trimString))
            StringTrimRight, string, string, %len%
    }
    return string
}


; WIP: Which version do you like more?!?!
; strips whitespace from start and end of a string:
string_strip(byref inputString)
{
    ; if first char is space, tab or linefeed, remove it and look again:
    c := SubStr(inputString, 1, 1)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimLeft, inputString, inputString, 1
        string_strip(inputString)
    }
    ; now last character:
    c := SubStr(inputString, 0)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimRight, inputString, inputString, 1
        string_strip(inputString)
    }

    return inputString
}

; Remove quotes from a string if necessary
string_unquote(string)
{
    if (InStr(string, """") = 1 && string_endsWith(string, """"))
        return string_trim(string, """")
    return string
}

; Add quotes to a string only if necessary
string_quote(string, once = 1)
{
    if (once)
    {
        if (InStr(string, """") != 1)
            string := """" string
        if (!string_endsWith(string, """"))
            string := string """"
        return string
    }
    return """" string """"
}
