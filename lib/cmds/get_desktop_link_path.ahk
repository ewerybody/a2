; Return target path of a2ui.lnk on users desktop.

link_path := A_Desktop "\a2ui.lnk"
if FileExist(link_path)
    FileGetShortcut link_path, &OutTarget
else
    OutTarget := ""
FileAppend(OutTarget, "*")
