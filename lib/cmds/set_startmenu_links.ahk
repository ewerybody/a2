; set windows start menu shortcuts
num_args = %0%
If num_args != 2
{
    MsgBox 0: %0%
    Return
}

a2dir = %1%
state = %2%

IfNotExist %a2dir%
{
    MsgBox a2dir: %a2dir% ??
    Return
}


start_menu_dir := A_Programs "\a2\"
a2_targets := ["a2.exe", "a2ui.exe", "Uninstall a2.exe", ""]
link_names := ["Start a2 Runtime", "Open a2 UI", "Uninstall a2", "Explore a2 Directory"],

; msgbox a2dir: %a2dir%`nstate: %state%`nstart_menu_dir: %start_menu_dir%

if (state) {
    FileCreateDir, %start_menu_dir%
    for i, target in a2_targets {
        this_path := a2dir "\" target
        link_path := start_menu_dir . link_names[i] . ".lnk"
        FileCreateShortcut, %this_path%, %link_path%, %a2dir%
        ; msgbox create link:`nthis_path: %this_path%`nlink_path: %link_path%`nErrorLevel: %ErrorLevel%
    }
}
Else {
    for i, link_name in link_names {
        link_path := start_menu_dir . link_name . ".lnk"
        FileDelete, %link_path%
    }
    if path_is_empty(start_menu_dir)
        FileRemoveDir, %start_menu_dir%
}
