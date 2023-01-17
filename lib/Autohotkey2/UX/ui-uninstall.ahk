; This script shows a GUI for uninstalling AutoHotkey or specific versions.
#include inc\bounce-v1.ahk
/* v1 stops here */
#requires AutoHotkey v2.0

#include inc\ui-base.ahk
#include install.ahk

#NoTrayIcon
#SingleInstance Force

A_ScriptName := "AutoHotkey Setup"
SetRegView 64
ModifySetupGui.Show()

class ModifySetupGui extends AutoHotkeyUxGui {
    __new() {
        super.__new(A_ScriptName, '-MinimizeBox -MaximizeBox')
        
        this.inst := Installation()
        this.inst.ResolveInstallDir()
        versions := this.inst.GetComponents()

        this.AddText(, "Remove which versions?")
        iv := this.AddListView('vComponents Checked -Hdr R10 w248', ["Version"])
        iv.OnEvent('ItemCheck', 'Checked')
        for v, files in versions
            iv.Add(files.HasProp('superseded') ? 'Check' : '', v)
        
        anyChecked := iv.GetNext(0, 'C')
        this.AddButton('vRemoveAll w120 ' (anyChecked ? '' : 'Default'), "Remove &all")
        .OnEvent('Click', 'ClickedRemove')
        this.AddButton('vRemove w120 yp ' (anyChecked ? 'Default' : 'Disabled'), "Remove &checked")
        .OnEvent('Click', 'ClickedRemove')
        
        if !this.inst.UserInstall && !A_IsAdmin {
            SendMessage 0x160C,, true, 'Button1', this ; BCM_SETSHIELD := 0x160C
            SendMessage 0x160C,, true, 'Button2', this
        }
    }
    
    ClickedRemove(btn, *) {
        cmd := ''
        if btn.Name = 'Remove' {
            n := 0, iv := this['Components'], count := 0
            while n := iv.GetNext(n, 'C')
                cmd .= ',' iv.GetText(n), ++count
            if count = iv.GetCount()
                cmd := '' ; All are selected - do a full uninstall
            else
                cmd := ' "' SubStr(cmd, 2) '"'
        }
        cmd := Format('"{1}" "{2}\install.ahk" /uninstall{3}', A_AhkPath, A_ScriptDir, cmd)
        if (!this.inst.UserInstall || A_Args.Length && A_Args[1] = '/elevate') && !A_IsAdmin
            cmd := '*RunAs ' cmd
        try {
            Run cmd
            ExitApp
        }
        catch as e
            if !InStr(e.Message e.Extra, 'cancel')
                throw e
    }
    
    Checked(iv, *) {
        this['Remove'].Enabled := iv.GetNext(0, 'C')
    }
}