
/**
 * Assemble a single string from an array of strings.
 * @param {(Array)} array_of_strings
 * Array of strings to join.
 * @param {(String)} [separator]
 * String to place between items. Defaults to ", ".
 * @param {(String)} [default]
 * Value to use for missing array items. Defaults to "".
 * @returns {(String)}
 * Joined string.
 */
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

/**
 * Search for a string in an array, returning its index.
 * @param {(String)} search
 * String to search for.
 * @param {(Array)} string_list
 * Array of strings to search in.
 * @param {(Integer)} [start]
 * Index to start searching from. Defaults to 1.
 * @returns {(Integer)}
 * Index of the match, or 0 if not found.
 */
string_is_in_array(search, string_list, start := 1) {
    Loop(string_list.Length) {
        idx := A_Index + start - 1
        if idx > string_list.Length
            Return 0
        if (search == string_list[idx])
            Return idx
    }
    Return 0
}

/**
 * Check if a string looks like a web address.
 * @param {(String)} string
 * String to check.
 * @returns {(Boolean)}
 * True if the string looks like a URL or web domain.
 */
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

/**
 * Check if a string starts with another string.
 * @param {(String)} string
 * String to check.
 * @param {(String)} start_str
 * Prefix to look for.
 * @returns {(Boolean)}
 * True if string starts with start_str.
 */
string_startswith(string, start_str) {
    return InStr(string, start_str) = 1
}

/**
 * Check if a string ends with another string.
 * @param {(String)} string
 * String to check.
 * @param {(String)} end
 * Suffix to look for.
 * @returns {(Boolean)}
 * True if string ends with end.
 */
string_endswith(string, end) {
    return StrLen(end) <= StrLen(string) && Substr(string, -StrLen(end)) = end
}

/**
 * Strip characters from both ends of a string.
 * @param {(String)} string
 * String to strip.
 * @param {(String)} [omit_chars]
 * Characters to remove. Defaults to whitespace.
 * @returns {(String)}
 * Stripped string.
 */
string_strip(string, omit_chars := "") {
    if omit_chars == ""
        omit_chars := " `t`n`r"
    return Trim(string, omit_chars)
}

/**
 * Strip characters from the right end of a string.
 * @param {(String)} string
 * String to strip.
 * @param {(String)} [omit_chars]
 * Characters to remove. Defaults to whitespace.
 * @returns {(String)}
 * Stripped string.
 */
string_strip_right(string, omit_chars := "") {
    if omit_chars == ""
        omit_chars := " `t`n`r"
    return RTrim(string, omit_chars)
}

/**
 * Strip characters from the left end of a string.
 * @param {(String)} string
 * String to strip.
 * @param {(String)} [omit_chars]
 * Characters to remove. Defaults to whitespace.
 * @returns {(String)}
 * Stripped string.
 */
string_strip_left(string, omit_chars := "") {
    if omit_chars == ""
        omit_chars := " `t`n`r"
    return LTrim(string, omit_chars)
}

/**
 * Remove surrounding quotes from a string if present.
 * @param {(String)} string
 * String to unquote.
 * @param {(String)} [quote]
 * Quote character to remove. Defaults to double-quote.
 * @returns {(String)}
 * Unquoted string, or the original if not quoted.
 */
string_unquote(string, quote := '"') {
    if (InStr(string, quote) = 1 && string_endsWith(string, quote))
        string := string_strip(string, quote)
    return string
}

/**
 * Surround a string with quotes, optionally only where missing.
 * @param {(String)} string
 * String to quote.
 * @param {(Integer)} [once]
 * If true, only add quotes where missing. Defaults to true.
 * @param {(String)} [quote]
 * Quote character to use. Defaults to double-quote.
 * @returns {(String)}
 * Quoted string.
 */
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

/**
 * Ensure a string ends with the given suffix, adding it if missing.
 * @param {(String)} string
 * String to check.
 * @param {(String)} suffix
 * Suffix to ensure.
 * @returns {(String)}
 * String guaranteed to end with suffix.
 */
string_suffix(string, suffix) {
    if !string_endswith(string, suffix)
        return string suffix
    return string
}

/**
 * Ensure a string starts with the given prefix, adding it if missing.
 * @param {(String)} string
 * String to check.
 * @param {(String)} prefix
 * Prefix to ensure.
 * @returns {(String)}
 * String guaranteed to start with prefix.
 */
string_prefix(string, prefix) {
    if !string_startswith(string, prefix)
        return prefix string
    return string
}

/**
 * Return a reversed copy of the given string.
 * @param {(String)} string
 * String to reverse.
 * @returns {(String)}
 * Reversed string.
 */
string_reverse(string) {
    new_string := ""
    Loop(StrLen(string))
        new_string := SubStr(string, A_Index, 1) new_string
    Return new_string
}

/**
 * Generate a random string of uppercase ASCII letters.
 * @param {(Integer)} length
 * Number of characters to generate.
 * @returns {(String)}
 * Random uppercase string of the given length.
 */
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

/**
 * Get number of occurrences in given string.
 * @param {(String)} string
 * Input string. "Haystack" so to say.
 * @param {(String)} what_to_count
 * String to count. "Needle" so to say.
 * @returns {(Integer)}
 * Number of found occurrences.
 */
string_count(string, what_to_count, case_sense := 0) {
    StrReplace(string, what_to_count, what_to_count, case_sense, &count)
    return count
}

/**
 * Get number of lines in given string.
 * @param {(String)} string
 * Input string. "Haystack" so to say.
  * @returns {(Integer)}
 * Number of found lines. Will at least be 1 line.
 */
string_count_lines(string) {
    return string_count(string, "`n") + 1
}