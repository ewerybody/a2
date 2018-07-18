; Source: https://github.com/ahkscript/libcrypt.ahk/blob/master/src/URI.ahk
; Modified by GeekDude from http://goo.gl/0a0iJq
lc_uri_encode(Uri, RE="[0-9A-Za-z]") {
    VarSetCapacity(Var, StrPut(Uri, "UTF-8"), 0), StrPut(Uri, &Var, "UTF-8")
    While Code := NumGet(Var, A_Index - 1, "UChar")
        Res .= (Chr:=Chr(Code)) ~= RE ? Chr : Format("%{:02X}", Code)
    Return, Res
}
