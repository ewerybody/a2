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
