; get_scope_nfo - returns all currently available window titles, classes and procresses in a string
; separated by linebreaks
WinGet, ids, list
data := ""
loop %ids% {
    thisId := ids%A_Index%
	WinGetTitle, this_title, ahk_id %thisId%
	WinGetClass, this_class, ahk_id %thisId%
    WinGet, this_proc, ProcessName, ahk_id %thisId%
    ;data = %data%t:%this_title%`nc:%this_class%`np:%this_proc%`n
    data = %data%%this_title%`n%this_class%`n%this_proc%`n
}
;msgbox data:`n>%data%<
FileAppend, %data%, *
