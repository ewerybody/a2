#requires AutoHotkey v2.0

#NoTrayIcon
#SingleInstance Off

#include inc\common.ahk
#include inc\ui-base.ahk

class NewScriptGui extends AutoHotkeyUxGui {
    __new(path:="") {
        super.__new("New Script")
        
        SplitPath path,, &dir,, &name
        if this.ExplorerHwnd := WinActive("ahk_class CabinetWClass") {
            this.Opt '+Owner' this.ExplorerHwnd
            if dir = ""
                dir := GetPathForExplorerWindow(this.ExplorerHwnd)
        }
        if dir = ""
            dir := ConfigRead('New', 'DefaultDir', A_MyDocuments "\AutoHotkey")
        
        name := this.AddEdit('vName w272', name != "New AutoHotkey Script" ? name : "")
        static EM_SETCUEBANNER := 0x1501
        SendMessage(EM_SETCUEBANNER, true, StrPtr("Untitled"), name)
        
        static IconSize := SysGet(49) ; SM_CXSMICON
        
        static BrowseIcon := LoadPicture("imageres.dll", 'Icon-1025 w' IconSize, &imgtype)
        this.AddIconButton('vBrowse x+0 yp-1 w28 hp+2', BrowseIcon, "&Browse")
        .OnEvent('Click', 'Browse')
        
        this.AddEdit('vDir xm w300 r1 ReadOnly -TabStop', dir)
        
        static LVS_SHOWSELALWAYS := 8 ; Seems to have the opposite effect with Explorer theme, at least on Windows 11.
        lv :=  this.AddListMenu("vLV xm w300 -" LVS_SHOWSELALWAYS, ["Name", "Desc", "Path", "Exec"])
        lv.OnEvent('DoubleClick', 'DoubleClicked')
        lv.OnEvent('ContextMenu', 'RightClicked')
        
        deft := GetDefaultTemplate()
        lv.Add(deft = "" ? 'Select' : '', "Empty", "Clean slate")
        for ,t in this.Templates := GetScriptTemplates() {
            if ConfigRead('New\HideTemplate', t.name, false)
                continue
            lv.Add(deft = t.name ? 'Select Focus' : '', t.name, t.desc)
        }
        
        lv.AutoSize(8)
        lv.GetPos(&x, &y, &w, &h)
        
        static DefaultsIcon := LoadPicture("imageres.dll", 'Icon-114 w' IconSize, &imgtype)
        this.AddIconButton('vDefaults r1 w28 xm y' y + h + this.MarginY, DefaultsIcon, "&Defaults")
        .OnEvent('Click', 'ChangeDefaults')
        
        this.AddButton('vCreate yp w75 x150', "&Create").OnEvent('Click', 'Confirm')
        this.AddButton('vEdit Default yp wp xm+225', "&Edit").OnEvent('Click', 'Confirm')
        if ConfigRead('New', 'DefaultButton', 'Edit') = 'Create'
            this['Create'].Opt('Default')
        
        if this.ExplorerHwnd {
            this.Show('AutoSize Hide')
            WinGetPos(,, &gw, &gh, this)
            WinGetPos(&x, &y, &ew, &eh)
            WinMove(x + (ew - gw) // 2, y + (eh - gh) // 2,,, this)
        }
    }
    
    static __new() {
        OnMessage(WM_KEYDOWN := 0x100, KeyDown)
        KeyDown(wParam, lParam, nmsg, hwnd) {
            static VK_UP := 0x26
            static VK_DOWN := 0x28
            if !(wParam = VK_UP || wParam = VK_DOWN)
                return
            g := GuiFromHwnd(hwnd, true)
            if g is NewScriptGui && g.FocusedCtrl is Gui.Edit {
                PostMessage nmsg, wParam, lParam, g['LV']
                return true
            }
        }
    }
    
    Browse(*) {
        path := this.FileSelect('S', this['Dir'].Value "\" this['Name'].Value, this.Title, "Script Files (*.ahk)")
        if path = ""
            return
        SplitPath path, &name, &dir
        this['Name'].Value := name
        this['Dir'].Value := dir
        this['LV'].Focus()
    }
    
    ChangeDefaults(btn, *) {
        lv := this["LV"]
        
        m := Menu()
        m.Add "Default to Create", setDefBtn, "Radio"
        m.Add "Default to Edit", setDefBtn, "Radio"
        m.Add "Stay open", toggleStayOpen
        if stayOpen := ConfigRead('New', 'StayOpen', false)
            m.Check "Stay open"
        m.Add
        m.Add "Set folder as default", (*) => SetDefaultDir(this['Dir'].Value)
        if this['Dir'].Value = GetDefaultDir()
            m.Check "Set folder as default"
        m.Add "Open templates folder", (*) => OpenTemplatesFolder()
        
        static DM_GETDEFID := 0x400
        m.Check (1 + (SendMessage(DM_GETDEFID,,, this) & 0xFFFF = DllCall('GetDlgCtrlID', 'ptr', this['Edit'].Hwnd))) "&"
        
        this.Opt "-DPIScale"
        btn.GetPos &x, &y, &w, &h
        ;btn.Focus ; This would also apply the "default" style, which would not revert correctly.
        ControlFocus btn
        m.Show x, y + h
        
        setDefBtn(itemname, itempos, *) {
            itemname := SubStr(itemname, 12)
            this[itemname].Opt('Default')
            ConfigWrite(itemname, 'New', 'DefaultButton')
        }
        toggleStayOpen(*) {
            ConfigWrite(stayOpen := !stayOpen, 'New', 'StayOpen')
        }
    }
    
    Confirm(btn, *) {
        lv := this['LV']
        if !index := lv.GetNext()
            return MsgBox("You need to select a template first.",, 'icon!')
        t := index = 1 ? '' : this.Templates[lv.GetText(index)]
        
        stayOpen := GetKeyState('Ctrl') || ConfigRead('New', 'StayOpen', false)
        
        DirCreate dir := this['Dir'].Value
        basename := this['Name'].Value
        (basename != '') || basename := "Untitled"
        SubStr(basename, -4) = ".ahk" && basename := SubStr(basename, 1, -4)
        newPath := dir "\" basename ".ahk"
        while FileExist(newPath)
            newPath := dir "\" basename "-" A_Index ".ahk"
        
        if t && t.execute
            RunWait Format('"{1}" "{2}" {3}', t.path, newPath, btn.Name), dir
        else {
            code := t = '' ? '' : FileRead(t.path)
            code := RegExReplace(code, 'si)/\*\s+\[NewScriptTemplate\].*\*/\R?')
            FileOpen(newPath, 'w', 'UTF-8').Write(code)
        }
        
        if this.ExplorerHwnd && (xp := GetExplorerByHwnd(this.ExplorerHwnd))
            || dir = A_Desktop && (xp := GetExplorerForDesktop()) {
            SplitPath newPath, &basename
            SelectExplorerItem xp, basename
        }
        else if btn.Name != 'Edit'
            Run 'explorer /select,"' newPath '"'
        
        if btn.Name = 'Edit'
            Run 'edit "' newPath '"'
        
        if !stayOpen
            this.Hide
    }
    
    RightClicked(lv, item, isRClick, x, y) {
        if !item
            return
        t := item > 1 ? this.Templates[lv.GetText(item)] : {name: ''}
        
        m := Menu()
        if item > 1 {
            m.Add "&Edit template", (*) => EditTemplate(t)
            m.Add "&Hide template", hideTemplate
        }
        m.Add "Set as &default", (*) => SetDefaultTemplate(t.name)
        if t.name = GetDefaultTemplate()
            m.Check "Set as &default"
        m.Show x, y
        
        hideTemplate(*) {
            ConfigWrite(true, 'New\HideTemplate', t.name)
            lv.Delete item
            static LVM_ARRANGE := 0x1016
            SendMessage LVM_ARRANGE,,, lv ; Fill in any gap left by item (in Tile view).
        }
    }
    
    DoubleClicked(lv, row) {
        if row
            this.Confirm(this.GetDefaultButton())
    }
    
    GetDefaultButton() {
        static DM_GETDEFID := 0x400
        hwnd := DllCall("GetDlgItem", "ptr", this.hwnd, "int", SendMessage(DM_GETDEFID,,, this) & 0xFFFF, "uint")
        return hwnd && this[hwnd]
    }
}

class NewScriptTemplate {
    __new(path, name:="", description:="") {
        this.path := path
        if name = ""
            SplitPath path,,,, &name
        this.name := name
        this.desc := IniRead(path, 'NewScriptTemplate', 'Description', description)
        this.execute := false
        switch IniRead(path, 'NewScriptTemplate', 'Execute', false) {
        case true, "true": this.execute := true
        }
    }
}

OpenTemplatesFolder() {
    dir := GetUserTemplateFolder(true)
    if dir != ""
        Run dir "\"
}

GetUserTemplateFolder(checkAndPrompt:=false) {
    static dir := A_MyDocuments "\AutoHotkey\Templates"
    if checkAndPrompt && !FileExist(dir) {
        if MsgBox("User-created templates should be placed in the following folder, "
                "which does not yet exist:`n`n" dir "`n`nCreate it now?",, "YesNo") = "No"
            return
        DirCreate dir
    }
    return dir
}

EditTemplate(t) {
    dir := GetUserTemplateFolder(true)
    if dir = ""
        return
    userPath := dir "\" t.name ".ahk"
    if !FileExist(userPath) {
        FileCopy t.path, userPath
        t.path := userPath
    }
    Run 'edit "' userPath '"'
}

GetScriptTemplates() {
    tmap := Map(), tmap.CaseSense := "off"
    sources := [
        A_ScriptDir "\Templates",
        GetUserTemplateFolder()
    ]
    if FileExist(t := A_WinDir '\ShellNew\Template.ahk')
        tmap["Legacy"] := NewScriptTemplate(t, "Legacy", "From " A_WinDir "\ShellNew")
    for source in sources {
        loop files source "\*.ahk" {
            t := NewScriptTemplate(A_LoopFilePath)
            tmap[t.name] := t
        }
    }
    return tmap
}

SetDefaultTemplate(t) => ConfigWrite(t = "Empty" ? "" : t, 'New', 'DefaultTemplate')
GetDefaultTemplate() => ConfigRead('New', 'DefaultTemplate', "")

SetDefaultDir(dir) => ConfigWrite(dir, 'New', 'DefaultDir')
GetDefaultDir() => ConfigRead('New', 'DefaultDir', A_MyDocuments "\AutoHotkey")

SelectExplorerItem(e, name) {
    sfv := e.Document
    if fi := sfv.Folder.ParseName(name)
        sfv.SelectItem(fi, 1|4|8|16)
    return e
}

GetExplorerByHwnd(hwnd) {
    for window in ComObject("Shell.Application").Windows
        if window.hwnd = hwnd
            return window
}

GetExplorerForDesktop() {
    hwndBuf := Buffer(4, 0), hwndRef := ComValue(0x4003, hwndBuf.Ptr)
    return ComObject("Shell.Application").Windows.FindWindowSW(0, "", 8, hwndRef, 1)
}

GetPathForExplorerWindow(hwnd) {
    try return GetExplorerByHwnd(hwnd).Document.Folder.Self.Path
}

GetExplorerByPath(path) {
    for window in ComObject("Shell.Application").Windows
        try if window.Document.Folder.Self.Path = path
            return window
    return ""
}

if A_ScriptFullPath = A_LineFile
    NewScriptGui.Show(A_Args.Length ? A_Args[1] : "")
