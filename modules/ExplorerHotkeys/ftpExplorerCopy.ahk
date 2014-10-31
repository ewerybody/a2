ftpExplorerCopy()
{
	WinGet, this_id, ID, A
	ControlGetText, path, ToolbarWindow322, ahk_id %this_id%

	if (SubStr(path, 1, 9) == "Adresse: ")
		StringTrimLeft, path, path, 9

	sel := Explorer_GetSelected(this_id)

	clip =

	; bend ftp paths to http:
	if Substr(path, 1, 6) == "ftp://"
	{
		
		@ := inStr(path,"@")
		if @
		{
			if sel
			{
				loop, parse, sel, `n,`r
					clip := clip "http://" SubStr(A_LoopField,@ + 1) "`n"
			}
		}
	}

	StringTrimRight, clip, clip, 1
	Clipboard := clip
	tt(clip,1)
}

/*
   Library for getting info from a specific explorer window (if window handle not specified, the currently active
   window will be used).  Requires AHK_L or similar.  Works with the desktop.  Does not currently work with save
   dialogs and such.
   
   
   Explorer_GetSelected(hwnd="")   - paths of target window's selected items
   Explorer_GetAll(hwnd="")        - paths of all items in the target window's folder
   Explorer_GetPath(hwnd="")       - path of target window's folder
   
   example:
      F1::
         path := Explorer_GetPath()
         all := Explorer_GetAll()
         sel := Explorer_GetSelected()
         MsgBox % path
         MsgBox % all
         MsgBox % sel
      return
   
   Joshua A. Kinnison
   2010-12-04, 14:39
*/

Explorer_GetPath(hwnd="")
{
   if !(window := Explorer_GetWindow(hwnd))
      return ErrorLevel := "ERROR"
   if (window="desktop")
      return A_Desktop
   path := window.LocationURL
   path := SubStr(path,InStr(path,"///")+3)
   StringReplace, path, path, /, \, All
   
   ; thanks to polyethene
   Loop
      If RegExMatch(path, "i)(?<=%)[\da-f]{1,2}", hex)
         StringReplace, path, path, `%%hex%, % Chr("0x" . hex), All
      Else Break
   return path
}
Explorer_GetAll(hwnd="")
{
   return Explorer_Get(hwnd)
}
Explorer_GetSelected(hwnd="")
{
   return Explorer_Get(hwnd,true)
}

Explorer_GetWindow(hwnd="")
{
   ; thanks to jethrow for some pointers here
    WinGet, process, processName, % "ahk_id" hwnd := hwnd? hwnd:WinExist("A")
    WinGetClass class, ahk_id %hwnd%
   
   if (process!="explorer.exe")
      return
   if (class ~= "(Cabinet|Explore)WClass")
   {
      for window in ComObjCreate("Shell.Application").Windows
         if (window.hwnd==hwnd)
            return window
   }
   else if (class ~= "Progman|WorkerW")
      return "desktop" ; desktop found
}
Explorer_Get(hwnd="",selection=false)
{
   if !(window := Explorer_GetWindow(hwnd))
      return ErrorLevel := "ERROR"
   if (window="desktop")
   {
      ControlGet, hwWindow, HWND,, SysListView321, ahk_class Progman
      if !hwWindow ; #D mode
         ControlGet, hwWindow, HWND,, SysListView321, A
      ControlGet, files, List, % ( selection ? "Selected":"") "Col1",,ahk_id %hwWindow%
      base := SubStr(A_Desktop,0,1)=="\" ? SubStr(A_Desktop,1,-1) : A_Desktop
      Loop, Parse, files, `n, `r
      {
         path := base "\" A_LoopField
         IfExist %path% ; ignore special icons like Computer (at least for now)
            ret .= path "`n"
      }
   }
   else
   {
      if selection
         collection := window.document.SelectedItems
      else
         collection := window.document.Folder.Items
      for item in collection
         ret .= item.path "`n"
   }
   ;return Trim(ret,"`n")
   return ret
}