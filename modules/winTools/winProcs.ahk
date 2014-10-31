
DetectHiddenWindows, Off
WinGet, Ids, list,,,Program Manager
; MsgBox rex_ids:%rex_ids%
winArray := {}
txt := "num windows: " Ids "`n"
; create process dict
; {'proc1':{'id1':'title1', 'id12':'title12'}, 'proc2':{'id2':'title2', 'id22':'title22'}}
Loop %Ids% {
	thisId := Ids%A_Index%
	WinGet, thisProcess, ProcessName, ahk_id %thisId%
	WinGetTitle thisTitle, ahk_id %thisId%
	if winArray.hasKey(thisProcess)
		winArray[thisProcess][thisId] := thisTitle
	else
		winArray[thisProcess] := {thisId:thisTitle}
}

For proc, procDic in winArray {
	txt := "proc: " proc ":`n"
	For id, title in winArray[proc] {
		txt := txt winArray[proc][id] "`n"
	}

	Menu, winProcMenu, Add, %proc%, getWinfoMenuHandler
}

Menu, winProcMenu, Show

Return
getWinfoMenuHandler:
	title := A_ThisMenuItem
	MsgBox title:%title%
return
