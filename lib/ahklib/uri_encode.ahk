;converts unicode_string to uri enocoded string for autohotkey_l unicode version	
; example
; keyword := uri_encode("测试")
; msgbox, An brower window will open searching for %keyword%.
; run, https://www.google.com/#newwindow=1&q=%keyword%&fp=1&bav=on.2,or.r_gc.r_pw.r_cp.,cf.osb&cad=b
;
; http://www.autohotkey.com/forum/viewtopic.php?t=71619
; https://autohotkey.com/board/topic/75390-ahk-l-unicode-uri-encode-url-encode-function/


uri_encode(Unicode_string)
{
    UTF16 := Unicode_string

    n := _uri_encode_StrPutVar(UTF16, UTF8, "UTF-8")
    raw_hex := _uri_encode_MCode_Bin2Hex(&UTF8, n-1)
    i := strlen(raw_hex)/2

    loop, %i%
        {
        frag := "%" . substr(raw_hex, a_index*2-1,2)
        r_s .= frag
        }
    return r_s
}


_uri_encode_MCode_Bin2Hex(addr, len) {
    Static fun
    If (fun = "") {
        If Not A_IsUnicode
        h=
        ( LTrim Join
            8B54240C85D2568B7424087E3A53578B7C24148A07478AC8C0E90480F9090F97C3F6
            DB80E30702D980C330240F881E463C090F97C1F6D980E10702C880C130880E464A75
            CE5F5BC606005EC3
        )
        Else
        h=
        ( LTrim Join
            8B44240C8B4C240485C07E53568B74240C578BF88A168AC2C0E804463C090FB6C076
            066683C037EB046683C03066890180E20F83C10280FA09760C0FB6D26683C2376689
            11EB0A0FB6C26683C03066890183C1024F75BD33D25F6689115EC333C0668901C3
        )
        VarSetCapacity(fun, n := StrLen(h)//2)
        Loop % n
            NumPut("0x" . SubStr(h, 2 * A_Index - 1, 2), fun, A_Index - 1, "Char")
    }
    VarSetCapacity(hex, A_IsUnicode ? 4 * len + 2 : 2 * len + 1)
    DllCall(&fun, "uint", &hex, "uint", addr, "uint", len, "cdecl")
    VarSetCapacity(hex, -1) ;update StrLen
    Return hex
}


_uri_encode_StrPutVar(string, ByRef var, encoding)
{
    VarSetCapacity( var, StrPut(string, encoding)
        * ((encoding="utf-16"||encoding="cp1200") ? 2 : 1) )
    return StrPut(string, &var, encoding)
}
