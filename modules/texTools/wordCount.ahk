wordCount() {
	txt := getSelection()
    words := StrSplit(txt, [A_Tab, A_Space, "`n", "`r"])
	StringLen, length, txt
    
    lines := StrSplit(txt, "`n")
	tt(length " Zeichen`n" words.maxIndex() " Worte`n" lines.maxIndex() " Zeilen", 5)
}