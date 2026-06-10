; set_windows_startup
#include <a2dlg>

If A_Args.Length != 2
{
    a2dlg_error("Need 2 arguments to set startup links!")
    Return
}
a2dir := A_Args[1]
state := A_Args[2]

If (!DirExist(a2dir))
{
    a2dlg_error("a2dir: " . a2dir . " ??")
    Return
}

link_path := A_Startup "\a2.lnk"

if (state) {
    a2_script_path := a2dir "\a2.exe"
    FileCreateShortcut(a2_script_path, link_path, a2dir)
} Else
    FileDelete(link_path)
