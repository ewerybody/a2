; Return target path of a2.lnk in Windows Startup Dir

link_path := A_Startup "\a2.lnk"
if FileExist(link_path)
    FileGetShortcut link_path, &OutTarget
else
    OutTarget := ""
FileAppend(OutTarget, "*")
