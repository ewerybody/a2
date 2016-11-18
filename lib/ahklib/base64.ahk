; ------------------------------------------------------------------------------
; http://www.autohotkey.com/forum/viewtopic.php?t=5896

A = 123-aB. ; TEST
Loop 8 {
    C := Base64Encode(A,A_Index)
    Base64Decode(D,C)
    VarSetCapacity(D,-1) ; use when D is string (instead of taking binary info)
    MsgBox % SubStr(A,1,A_Index) "`n" C "`n" D
}

Base64Encode(ByRef bin, n=0) {
   m := VarSetCapacity(bin)
   Loop % n<1 || n>m ? m : n
      A := *(&bin+A_Index-1)
     ,m := Mod(A_Index,3)
     ,b := m=1 ? A << 16 : m=2 ? b+(A<<8) : b+A
     ,out .= m ? "" : Code(b>>18) Code(b>>12) Code(b>>6) Code(b)
   Return out (m ? Code(b>>18) Code(b>>12) (m=1 ? "==" : Code(b>>6) "=") : "")
}
Code(i) {   ; <== Chars[i & 63], 0-base index
   Static Chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
   Return SubStr(Chars,(i&63)+1,1)
}

Base64Decode(ByRef bin, code) {
   Static Chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
   StringReplace code, code, =,, All
   VarSetCapacity(bin, 3*StrLen(code)//4, 0)
   pos = 0
   Loop Parse, code
      m := A_Index&3, d := InStr(Chars,A_LoopField,1) - 1
     ,b := m ? (m=1 ? d<<18 : b+(d<<24-6*m)) : b+d
     ,Append(bin, pos, 3*!m, b>>16, 255 & b>>8, 255 & b)
   Append(bin, pos, !!m+(m&1), b>>16, 255 & b>>8, 0)
}
Append(ByRef bin, ByRef pos, k, c1,c2,c3) {
   Loop %k%
      DllCall("RtlFillMemory",UInt,&bin+pos++, UInt,1, UChar,c%A_Index%)
}
