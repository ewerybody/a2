wordCount() {
	txt := getSelection()
	StringSplit, parts, txt, %A_Space%`n`r
	StringLen, length, txt
	tt(length " Zeichen`n" parts0 " Worte",5)
}