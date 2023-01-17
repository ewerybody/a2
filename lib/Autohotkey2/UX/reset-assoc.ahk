; This script clears any file type assocation made via the "open with" dialog,
; so that the standard registration under HKCR\.ahk can take effect.
#include inc\bounce-v1.ahk
/* v1 stops here */
#requires AutoHotkey v2.0

keyname := "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.ahk\UserChoice"
initial_progid := RegRead(keyname, "ProgId", "")
if A_Args.Length && A_Args[1] = '/check' {
    if initial_progid = "" || initial_progid = "AutoHotkeyScript"
        || MsgBox("It looks like you've used an unsupported method to set the default program for .ahk files. "
            . "This will prevent the standard context menu and launcher (version auto-detect) functionality "
            . "from working. Would you like this setting to be reset for you?", "AutoHotkey", "Icon! y/n") != "yes"
        ExitApp
}
reg_file_path := A_Temp "\reset-ahk-file-association.reg"
FileOpen(reg_file_path, "w").Write("Windows Registry Editor Version 5.00`n"
    . "[-" keyname "]`n")
EnvSet "__COMPAT_LAYER", "RunAsInvoker"
RunWait 'regedit.exe /S "' reg_file_path '"'
EnvSet "__COMPAT_LAYER", ""
DllCall("shell32\SHChangeNotify", "uint", 0x08000000, "uint", 0, "int", 0, "int", 0) ; SHCNE_ASSOCCHANGED
FileDelete reg_file_path
new_progid := RegRead(keyname, "ProgId", "")
if (new_progid != "" || A_LastError != 2)
    MsgBox "Something went wrong and the reset probably "
        . "didn't work.`n`nCurrent association: "
        . (new_progid = "" ? "(unknown)" : new_progid), "AutoHotkey", "Icon!"
else if (initial_progid != "")
    MsgBox "Association of .ahk files for the current user has been reset.", "AutoHotkey", "Iconi"
else
    MsgBox "It looks as though the current user's settings "
        . "weren't overriding the default .ahk file options. A reset was "
        . "attempted anyway, but it probably had no effect.", "AutoHotkey", "Icon!"