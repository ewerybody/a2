ftpExplorerCopy()
{
	WinGet, this_id, ID, A
	;legacy: Win 7: ;ControlGetText, path, ToolbarWindow322, ahk_id %this_id%
    ;Win 8 ;ControlGetText, path, ToolbarWindow323, ahk_id %this_id%

	sel := Explorer_GetSelected(this_id)
	clip := ""
    if sel
    {
        loop, parse, sel, `n,`r
        {
            if Substr(A_LoopField, 1, 6) == "ftp://"
            {
                posAt := InStr(A_LoopField,"@")
                clip := clip "http://" SubStr(A_LoopField, posAt + 1) "`n"
            }
        }
    }
    else
    {
        tt("Nothing selected!", 1)
        Return
    }

	StringTrimRight, clip, clip, 1
	Clipboard := clip
	tt(clip, 1)
}
