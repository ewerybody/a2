; get_scope_nfo - returns all currently available window titles, classes and procresses in a string
; separated by linebreaks
data := ""
For this_id in WinGetList() {
	this_title := WinGetTitle("ahk_id " . this_id)
	this_class := WinGetClass("ahk_id " . this_id)
    this_proc := WinGetProcessName("ahk_id " . this_id)
    data .= this_title "`n" this_class "`n" this_proc "`n"
}
FileAppend(data, "*")
