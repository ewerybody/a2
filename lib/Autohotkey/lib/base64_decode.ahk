; ------------------------------------------------------------------------------
; http://www.autohotkey.com/forum/viewtopic.php?t=5896

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
