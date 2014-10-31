;winHook_SearchList := [] ;
winHook_SearchList := [{title: "Change Name", class: "#32770", process: "Editor.exe", action: "toCursor"}] ;
x := winHook_SearchList[1]["title"]
MsgBox x:%winHook_SearchList[1]["title"]%