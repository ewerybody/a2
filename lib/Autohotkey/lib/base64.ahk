; ------------------------------------------------------------------------------
; http://www.autohotkey.com/forum/viewtopic.php?t=5896
/*
A = 123-aB. ; TEST
Loop 8 {
    C := base64_encode(A,A_Index)
    base64_decode(D,C)
    VarSetCapacity(D,-1) ; use when D is string (instead of taking binary info)
    MsgBox % SubStr(A,1,A_Index) "`n" C "`n" D
}
*/

base64_encode(ByRef bin, n=0) {
   m := VarSetCapacity(bin)
   Loop % n<1 || n>m ? m : n
      A := *(&bin+A_Index-1)
     ,m := Mod(A_Index,3)
     ,b := m=1 ? A << 16 : m=2 ? b+(A<<8) : b+A
     ,out .= m ? "" : __base64_code(b>>18) __base64_code(b>>12) __base64_code(b>>6) __base64_code(b)
   Return out (m ? __base64_code(b>>18) __base64_code(b>>12) (m=1 ? "==" : __base64_code(b>>6) "=") : "")
}


__base64_code(i) {   ; <== Chars[i & 63], 0-base index
   Static Chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
   Return SubStr(Chars,(i&63)+1,1)
}


base64_decode(ByRef bin, code) {
   Static Chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
   StringReplace code, code, =,, All
   VarSetCapacity(bin, 3*StrLen(code)//4, 0)
   pos = 0
   Loop Parse, code
      m := A_Index&3, d := InStr(Chars,A_LoopField,1) - 1
     ,b := m ? (m=1 ? d<<18 : b+(d<<24-6*m)) : b+d
     ,__base64_append(bin, pos, 3*!m, b>>16, 255 & b>>8, 255 & b)
   __base64_append(bin, pos, !!m+(m&1), b>>16, 255 & b>>8, 0)
}


__base64_append(ByRef bin, ByRef pos, k, c1,c2,c3) {
   Loop %k%
      DllCall("RtlFillMemory",UInt,&bin+pos++, UInt,1, UChar,c%A_Index%)
}
