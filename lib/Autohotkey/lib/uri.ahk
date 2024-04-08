; libcrypt uri functions - Source: https://github.com/ahkscript/libcrypt.ahk/blob/master/src/URI.ahk
; Modified by GeekDude from http://goo.gl/0a0iJq
uri_url_encode(url) { ; keep ":/;?@,&=+$#."
    return uri_encode(url, "[0-9a-zA-Z:/;?@,&=+$#.]")
}


uri_decode(uri) {
    ; Find percentage encoding and turn it back to readable characters.
    ; "https%3A%2F%2F" -> "https://"
    Loop
    {
        ; find "%20" patterns. That's 2 hex digits after a %
        RegExMatch(uri, "i)(?<=%)[\da-f]{1,2}", &match)
        If (!match)
            Break
        uri := StrReplace(uri, "%" . match[0], Chr("0x" . match[0]))
    }
    Return uri

    ; Pos := 1
    ; While Pos := RegExMatch(uri, "i)(%[\da-f]{2})+", &Code, Pos)
    ; {
    ;     ; VarSetCapacity(Var, StrLen(Code) // 3, 0), Code := SubStr(Code,2)
    ;     VarSetStrCapacity(&Var, StrLen(Code[1]) // 3)
    ;     Loop Parse Code, "%"
    ;         NumPut("0x" A_LoopField, Var, A_Index-1, "UChar")
    ;     msgbox(Var)
    ;     Decoded := StrGet(&Var, "UTF-8")
    ;     uri := SubStr(uri, 1, Pos-1) . Decoded . SubStr(uri, Pos+StrLen(Code)+1)
    ;     Pos += StrLen(Decoded)+1
    ; }
    ; Return uri
}


uri_encode(uri, RE:="[0-9A-Za-z]") {
    ; Turn special characters to percentage encoding.
    ; VarSetCapacity(Var, StrPut(uri, "UTF-8"), 0)
    ; VarSetStrCapacity(&Var, StrPut(uri, "UTF-8"))
    ; StrPut(uri, Var, "UTF-8")

    var := Buffer(StrPut(uri, "UTF-8"))
    StrPut(uri, var, "UTF-8")

    Res := ""
    While Code := NumGet(Var, A_Index - 1, "UChar")
        Res .= (C:=Chr(Code)) ~= RE ? C : Format("%{:02X}", Code)
    Return Res
}
