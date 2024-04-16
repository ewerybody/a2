; to create of remove a desktop link to the a2 ui
#include <msgbox>
If A_Args.Length != 2
{
    msgbox_error("Need 2 arguments to set Desktop link!")
    Return
}

a2dir := A_Args[1]
state := A_Args[2]

If (!DirExist(a2dir))
{
    msgbox_error("a2dir: " . a2dir . " ??")
    Return
}

a2_script_path := a2dir "\a2ui.exe"
link_path := A_Desktop "\a2ui.lnk"

if (state)
    FileCreateShortcut(a2_script_path, link_path, a2dir)
Else
    FileDelete(link_path)
