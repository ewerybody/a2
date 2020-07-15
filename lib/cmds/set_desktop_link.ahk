; to create of remove a desktop link to the a2 ui
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

a2_script_path := a2dir "\a2ui.exe"
link_path := A_Desktop "\a2ui.lnk"

if (state)
    FileCreateShortcut, %a2_script_path%, %link_path%, %a2dir%
Else
    FileDelete, %link_path%
