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
string_is_web_adress(string) {
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
