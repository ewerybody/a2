; libcrypt uri functions - Source: https://github.com/ahkscript/libcrypt.ahk/blob/master/src/URI.ahk
; Modified by GeekDude from http://goo.gl/0a0iJq
uri_url_encode(url) { ; keep ":/;?@,&=+$#."
    return uri_encode(url, "[0-9a-zA-Z:/;?@,&=+$#.]")
}


; Find percentage encoding and turn it back to readable characters.
; "https%3A%2F%2F" -> "https://"
uri_decode(uri) {
    Loop
    {
        ; find "%20" patterns. That's 2 hex digits after a %
        RegExMatch(uri, "i)(?<=%)[\da-f]{1,2}", &match)
        If (!match)
            Break
        uri := StrReplace(uri, "%" . match[0], Chr("0x" . match[0]))
    }
    Return uri
}


; Turn special characters to percentage encoding.
uri_encode(uri, RE:="[0-9A-Za-z]") {
    var := Buffer(StrPut(uri, "UTF-8"))
    StrPut(uri, var, "UTF-8")

    Res := ""
    While Code := NumGet(Var, A_Index - 1, "UChar")
        Res .= (C:=Chr(Code)) ~= RE ? C : Format("%{:02X}", Code)
    Return Res
}
