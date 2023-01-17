; This script shows the initial setup GUI.
; It is not intended for use after installation.
#requires AutoHotkey v2.0

#NoTrayIcon
#SingleInstance Force

#include inc\ui-base.ahk

A_ScriptName := "AutoHotkey Setup"
SetRegView 64
InstallGui.Show()

class InstallGui extends AutoHotkeyUxGui {
    __new() {
        super.__new(A_ScriptName, '-MinimizeBox -MaximizeBox')
        
        DllCall('uxtheme\SetWindowThemeAttribute', 'ptr', this.hwnd, 'int', 1 ; WTA_NONCLIENT
            , 'int64*', 3 | (3<<32), 'int', 8) ; WTNCA_NODRAWCAPTION=1, WTNCA_NODRAWICON=2
        
        static TitleBack := 'BackgroundWhite'
        static TitleFore := 'c3F627F'
        static TotalWidth := 350
        this.AddText('x0 y0 w' TotalWidth ' h84 ' TitleBack)
        this.AddPicture('x32 y16 w32 h32 ' TitleBack, A_AhkPath)
        this.SetFont('s12', 'Segoe UI')
        this.AddText('x+20 yp+4 ' TitleFore ' ' TitleBack, "AutoHotkey v" A_AhkVersion)
        this.SetFont('s9')
        
        ; SS_SUNKEN := 0x1000 ; 4096
        this.AddText('x-4 y84 w' TotalWidth+4 ' h188 0x1000 -Background')
        
        this.AddText('xm yp+16', 'Install &to:')
        dirEdit := this.AddEdit('vInstallDir w' TotalWidth - (2 * this.MarginX) - 88)
        this.AddButton('vBrowseButton w80 x+8 yp-1', '&Browse')
        .OnEvent('Click', 'Browse')
        
        rect := Buffer(16, 0)
        DllCall('GetClientRect', 'ptr', dirEdit.hwnd, 'ptr', rect)
        NumPut('int', 4, 'int', 2, rect)
        ; DllCall('InflateRect', 'ptr', rect, 'int', 0, 'int', )
        EM_SETRECT := 0xB3 ; 179
        SendMessage 0xB3, 0, rect.ptr, dirEdit
        
        this.AddGroupBox('xm y+0 w' TotalWidth - (2 * this.MarginX) ' h44')
        this.AddText('xp+8 yp+16', "Install mode:")
        this.AddRadio('vModeAll x+m yp Checked', "&All users")
        .OnEvent('Click', 'ModeChange')
        this.AddRadio('vModeUser x+4', "&Current user")
        .OnEvent('Click', 'ModeChange')
        this.AddRadio('vModePortable x+4 Disabled', "Portable")
        .OnEvent('Click', 'ModeChange')
        
        this.AddButton('vInstallButton x' (TotalWidth - 80) // 2 ' w80 y+36 Default', "&Install")
        .OnEvent('Click', 'Install')
        
        this.ModeChange()
        
        this.MarginY := -1
        this.Show('Hide w' TotalWidth)
        this['InstallButton'].Focus()
    }
    
    Browse(*) {
        if ControlGetStyle(this['InstallDir']) & 0x800 { ; ES_READONLY
            rootKey := this['ModeAll'].Value ? 'HKLM' : 'HKCU'
            message := "Changing the installation directory is not recommended."
            if InStr(RegRead(rootKey '\Software\AutoHotkey', 'Version', ''), '1.') = 1
                message .= "`n`nThis installation package is designed to allow both v1 and v2 to be associated with .ahk files, but only if they are installed in the same directory."
            message .= "`n`nExisting files will not be moved."
            if MsgBox(message,, "OKCancel Icon!") != "OK"
                return
            this['InstallDir'].Opt('-ReadOnly')
        }
        dir := this.FileSelect('D', this['InstallDir'].Value '\', "Select installation directory")
        if dir != '' {
            this['InstallDir'].Value := dir
            this.InstallDirChange()
        }
    }
    
    ModeChange(p*) {
        if !this.CheckAlreadyInstalled(p.Length = 0, true) {
            ; Ensure InstallDir makes sense for the new mode
            static DefaultAllDir := (EnvGet('ProgramW6432') || A_ProgramFiles) '\AutoHotkey'
            static DefaultUserDir := EnvGet('LocalAppData') '\Programs\AutoHotkey'
            installDir := this['InstallDir'].Value
            if this['ModeAll'].Value {
                if installDir = '' || installDir = DefaultUserDir
                    this['InstallDir'].Value := DefaultAllDir, this['InstallDir'].Opt('-ReadOnly')
            } else
                if installDir = '' || IsInProgramFiles(installDir)
                    this['InstallDir'].Value := DefaultUserDir, this['InstallDir'].Opt('-ReadOnly')
        }
        this.UpdateShield()
    }
    
    InstallDirChange(*) {
        this.UpdateShield()
    }
    
    UpdateShield() {
        requireAdmin := this['ModeAll'].Value && !A_IsAdmin
        SendMessage 0x160C, 0, requireAdmin, this['InstallButton'] ; BCM_SETSHIELD
    }
    
    CheckAlreadyInstalled(setMode:=false, setDir:=false) {
        for rootKey in setMode ? ['HKCU', 'HKLM'] : [this['ModeAll'].Value ? 'HKLM' : 'HKCU'] {
            dir := RegRead(rootKey '\Software\AutoHotkey', 'InstallDir', '')
            if dir != '' {
                if setDir {
                    this['InstallDir'].Value := dir
                    this['InstallDir'].Opt('+ReadOnly')
                }
                if setMode
                    this[A_Index = 1 ? 'ModeUser' : 'ModeAll'].Value := true
                return dir
            }
        }
        return ''
    }
    
    Install(*) {
        problem := ''
        requireAdmin := this['ModeAll'].Value
        installDir := this['InstallDir'].Value
        buf := Buffer(260*2)
        n := DllCall('GetFullPathName', 'str', installDir, 'uint', 260, 'ptr', buf, 'ptr', 0)
        if !n || n > 259 {
            MsgBox "Please enter a valid path.",, 'Icon!'
            return
        }
        fullPath := StrGet(buf)
        if installDir != fullPath {
            problem .= '"' installDir '" resolves to "' fullPath '".`n`n'
            installDir := fullPath
        }
        dir := this.CheckAlreadyInstalled()
        if dir && dir != installDir
            problem .= 'The existing installation in "' dir '" will not be moved or integrated with the new installation.`n`n'
        if requireAdmin && !IsInProgramFiles(installDir) && dir != installDir
            problem .= 'Enabling UI Access will not be possible because the installation directory is not a sub-directory of Program Files. Without UI Access, non-elevated scripts cannot interact with windows of elevated programs.`n`n'
        if problem && MsgBox(problem,, 'OKCancel Default2 Icon!') = 'Cancel'
            return
        if A_IsCompiled && IsSet(Installation)
            cmd := Format('"{1}" /to "{2}"', A_ScriptFullPath, installDir)
        else
            cmd := Format('"{1}" /script "{2}\install.ahk" /to "{3}"', A_AhkPath, A_ScriptDir, installDir)
        if !requireAdmin
            cmd .= ' /user'
        else if !A_IsAdmin
            cmd := '*RunAs ' cmd
        try
            Run cmd,,, &pid
        catch as e {
            if A_LastError != 1223 ; ERROR_CANCELLED
                MsgBox e.Message "`n`n" e.Extra,, 'IconX'
        } else {
            this['InstallButton'].Enabled := false
            this['InstallButton'].Text := "Installing..."
            ProcessWaitClose pid
            ExitApp
        }
    }
}

IsInProgramFiles(path) {
    other := EnvGet(A_PtrSize=8 ? "ProgramFiles(x86)" : "ProgramW6432")
    return InStr(path, A_ProgramFiles "\") = 1
        || other && InStr(path, other "\") = 1
}