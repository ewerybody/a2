; Return target path of a2.lnk in Windows Startup Dir

link_path := A_Startup "\a2.lnk"
FileGetShortcut link_path, &OutTarget
FileAppend(OutTarget, "*")
