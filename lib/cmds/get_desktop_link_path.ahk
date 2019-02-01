; Returns the target path of a2ui.lnk in on users desktop.

link_path := A_Desktop "\a2ui.lnk"
FileGetShortcut, %link_path%, OutTarget
FileAppend, %OutTarget%, *
