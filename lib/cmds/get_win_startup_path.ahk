; Return target path of a2.lnk in Windows Startup Dir
; Which is usually:
;   C:\Users\{USERNAME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
; or:
;   %appdata%\Microsoft\Windows\Start Menu\Programs\Startup

link_path := A_Startup "\a2.lnk"
if FileExist(link_path)
    FileGetShortcut link_path, &OutTarget
else
    OutTarget := ""
FileAppend(OutTarget, "*")
