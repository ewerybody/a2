; Run this script to launch or download and install Ahk2Exe into A_ScriptDir '\..\Compiler'.
#requires AutoHotkey v2.0

#include install.ahk
#include inc\GetGitHubReleaseAssetURL.ahk

#SingleInstance Force
InstallAhk2Exe

InstallAhk2Exe() {
    inst := Installation()
    inst.ResolveInstallDir()  ; This sets inst.InstallDir and inst.UserInstall
    
    finalPath := inst.InstallDir '\Compiler\Ahk2Exe.exe'
    if FileExist(finalPath) {
        ShellRun finalPath
        ExitApp
    }
    
    if !A_Args.Length {
        (inst.UserInstall) || SetTimer(() => (
            WinExist('ahk_class #32770 ahk_pid ' ProcessExist()) &&
            SendMessage(0x160C,, true, 'Button1') ; BCM_SETSHIELD := 0x160C
        ), -25)
        if MsgBox("Ahk2Exe is not installed, but we can download and install it for you.", "AutoHotkey", 'OkCancel') = 'Cancel'
            ExitApp
        if !A_IsAdmin && !inst.UserInstall {
            Run Format('*RunAs "{1}" /restart /script "{2}" /Y', A_AhkPath, A_ScriptFullPath)
            ExitApp
        }
    }
    
    tempDir := A_ScriptDir '\.staging' ; Avoid A_Temp for security reasons
    DirCreate tempDir
    SetWorkingDir tempDir
    
    TrayTip "Downloading Ahk2Exe", "AutoHotkey"
    url := GetGitHubReleaseAssetURL('AutoHotkey/Ahk2Exe')
    Download url, 'Ahk2Exe.zip'
    
    TrayTip "Installing Ahk2Exe", "AutoHotkey"
    DirCopy 'Ahk2Exe.zip', 'Compiler', true
    FileDelete 'Ahk2Exe.zip'
    
    inst.AddCompiler(tempDir '\Compiler')
    inst.Apply()
    
    ; Working dir may have been changed
    DirDelete tempDir '\Compiler', true
    DirDelete tempDir
    
    ShellRun finalPath
}
