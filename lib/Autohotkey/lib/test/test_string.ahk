#Include %A_ScriptDir%\..\string.ahk
#Include a2test.ahk

; test join
aabc := ["a", "b", "c"]
joint := string_join(aabc, "||")
sabc := string_join(aabc, "")
arr := StrSplit(joint, "||")
res := ""
Loop, % arr.MaxIndex() {
    this := arr[A_Index]
    res = %res%%this%
}
j1 := assertmsg(sabc = res)
msg = string_join:%j1% test:>%sabc%< control:>%res%<`n

; Test quote/unquote
s := "'XfgfsgsdfgX'"
un := string_unquote(s, "'")
q1 := string_quote(un,,quote:="'")
q2 := assertmsg(s == q1)
q3 := string_quote(un,once:=1,quote:="'")
q4 := assertmsg(s == q3)
u1 := assertmsg(string_startswith(un, "X"))
u2 := assertmsg(string_endswith(un, "X"))
p := "C:\Users\eric\AppData\Local\Programs\Microsoft VS Code Insiders\Code - Insiders.exe"
pq := """" . p . """"
up := string_unquote(p)
ups := assertmsg(p == up)
msg .= "string_unquote ' :" u1 " " u2 "`n"
msg .= "string_unquote "" :" ups "`n"
msg .= "string_quote:" q2 " " q4 "`n"

; test is in array
i1 := assertmsg(string_is_in_array("b", aabc))
i2 := assertmsg(!string_is_in_array("B", aabc))
msg .= "string_is_in_array: " i1 " " i2 "`n"

; test suffixing
st := "Free Assange"
nstr := string_suffix(st, "!")
nst2 := string_suffix(nstr, "!")
s1 := assertmsg(st != nstr)
s2 := assertmsg(nst2 == nstr)
msg .= "string_suffix: " s1 " " s2

MsgBox, %msg%