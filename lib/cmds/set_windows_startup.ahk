; set_windows_startup
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

a2_script_path := a2dir "\a2.exe"
link_path := A_Startup "\a2.lnk"
ico_path := a2dir "\ui\a2.ico"

if %state%
{
    FileCreateShortcut, %a2_script_path%, %link_path%, %a2dir%,,,%ico_path%
}
Else
    FileDelete, %link_path%
