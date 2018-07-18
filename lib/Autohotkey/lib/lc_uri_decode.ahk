; Source: https://github.com/ahkscript/libcrypt.ahk/blob/master/src/URI.ahk
; Modified by GeekDude from http://goo.gl/0a0iJq
lc_uri_decode(Uri) {
    Pos := 1
    While Pos := RegExMatch(Uri, "i)(%[\da-f]{2})+", Code, Pos)
    {
        VarSetCapacity(Var, StrLen(Code) // 3, 0), Code := SubStr(Code,2)
        Loop, Parse, Code, `%
            NumPut("0x" A_LoopField, Var, A_Index-1, "UChar")
        Decoded := StrGet(&Var, "UTF-8")
        Uri := SubStr(Uri, 1, Pos-1) . Decoded . SubStr(Uri, Pos+StrLen(Code)+1)
        Pos += StrLen(Decoded)+1
    }
    Return, Uri
}
