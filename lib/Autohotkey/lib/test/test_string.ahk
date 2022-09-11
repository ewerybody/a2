#Include %A_ScriptDir%\..\string.ahk
#Include a2test.ahk

; test join
aabc := ["a", "b", "c"]
abcs := "abc"

joint := string_join(aabc, "||")
sabc := string_join(aabc, "")
arr := StrSplit(joint, "||")
res := ""
Loop, % arr.MaxIndex()
    res .= arr[A_Index]
j1 := assertmsg(sabc == abcs)
j2 := assertmsg(sabc == res)
msg = string_join:%j1% test:>%sabc%< control:>%abcs%<`n
; Test starts/endswith
; This is also case-INsensitive
sw1 := assertmsg(string_startswith("a#$ NCowehofd", "A#$ "))
sw2 := assertmsg(!string_startswith(" 3456 NCowehofd", " 3456  "))
msg .= "string_startswith ' :" sw1 " " sw2 "`n"

ew1 := assertmsg(string_endswith("NCowehofd$#%S", "$#%s"))
ew2 := assertmsg(!string_endswith("NCowehofd$#%", "9fh3"))
msg .= "string_endswith ' :" ew1 " " ew2 "`n"

; Test quote/unquote
s := "'XfgfsgsdfgX'"
un := string_unquote(s, "'")
q1 := string_quote(un,,quote:="'")
q2 := assertmsg(s == q1)
q3 := string_quote(un,once:=1,quote:="'")
q4 := assertmsg(s == q3)
u1 := assertmsg(string_startswith(un, "X"))
u2 := assertmsg(string_endswith(un, "X"))

p := A_ScriptFullPath
pq := """" . p . """"
up := string_unquote(p)
ups := assertmsg(p == up)
msg .= "string_unquote ' :" u1 " " u2 "`n"
msg .= "string_unquote "" :" ups "`n"
msg .= "string_quote:" q2 " " q4 "`n"

; test is in array
i1 := assertmsg(string_is_in_array("b", aabc))
i2 := assertmsg(!string_is_in_array("B", aabc))
i3 := assertmsg(!string_is_in_array("a", aabc, 2))
msg .= "string_is_in_array: " i1 " " i2 " " i3 "`n"

; test suffixing
st := "Free Assange"
nstr := string_suffix(st, "!")
nst2 := string_suffix(nstr, "!")
s1 := assertmsg(st != nstr)
s2 := assertmsg(nst2 == nstr)
msg .= "string_suffix: " s1 " " s2 "`n"

pstr := string_prefix(st, "Free")
s3 := assertmsg(st == pstr)
pstr2 := string_prefix(st, "!")
s4 := assertmsg(st != pstr2)
msg .= "string_prefix: " s3 " " s4 "`n"

; Test Reverse
st := "Test Reverse"
s1 := string_reverse(st)
s2 := assertmsg(st == string_reverse(s1))
msg .= "string_reverse: " st " " s2 " " s1 "`n"

MsgBox, %msg%