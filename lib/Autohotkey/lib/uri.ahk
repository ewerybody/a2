; libcrypt uri functions - Source: https://github.com/ahkscript/libcrypt.ahk/blob/master/src/URI.ahk
; Modified by GeekDude from http://goo.gl/0a0iJq
uri_url_encode(url) { ; keep ":/;?@,&=+$#."
    return uri_encode(url, "[0-9a-zA-Z:/;?@,&=+$#.]")
}


uri_decode(uri) {
    ; Find percentage encoding and turn it back to readable characters.
    ; "https%3A%2F%2F" -> "https://"
    Pos := 1
    While Pos := RegExMatch(uri, "i)(%[\da-f]{2})+", Code, Pos)
    {
        VarSetCapacity(Var, StrLen(Code) // 3, 0), Code := SubStr(Code,2)
        Loop, Parse, Code, `%
            NumPut("0x" A_LoopField, Var, A_Index-1, "UChar")
        Decoded := StrGet(&Var, "UTF-8")
        uri := SubStr(uri, 1, Pos-1) . Decoded . SubStr(uri, Pos+StrLen(Code)+1)
        Pos += StrLen(Decoded)+1
    }
    Return, uri
}


uri_encode(uri, RE="[0-9A-Za-z]") {
    ; Turn special characters to percentage encoding.
    VarSetCapacity(Var, StrPut(uri, "UTF-8"), 0), StrPut(uri, &Var, "UTF-8")
    While Code := NumGet(Var, A_Index - 1, "UChar")
        Res .= (Chr:=Chr(Code)) ~= RE ? Chr : Format("%{:02X}", Code)
    Return, Res
}
