; This script shows a GUI for setting the default .ahk editor.
#requires AutoHotkey v2.0

#NoTrayIcon
#SingleInstance Off

#include launcher.ahk
#include inc\CommandLineToArgs.ahk

class EditorSelectionGui extends AutoHotkeyUxGui {
    __new(cmdLine) {
        super.__new("Select an editor")
        
        lv := this.AddListMenu('vEds LV0x40 w300', ["Editor"])
        this.IconList := il := IL_Create(,, true)
        lv.SetImageList(il, 0)
        for app in this.Apps := GetEditorApps() {
            try
                icon := IL_Add(il, app.exe)
            catch
                icon := -1
            lv.Add('Icon' icon, app.name)
        }
        this.SelectEditorByCmd(cmdLine)
        lv.AutoSize(8)
        lv.GetPos(&x, &y, &w, &h)
        x += w
        y += h
        
        this.AddText('xm w' w ' y' y, "Command line")
        this.AddEdit('xm wp r2 -WantReturn vCmd', cmdLine).OnEvent('Change', 'CmdChanged')
        
        this.AddText('xm h25 18 w' w)
        this.AddPicture('x56 Icon-81 w16 yp+4', "imageres.dll")
        this.AddLink('x76 yp-1', "<a>Editors with AutoHotkey support</a>")
            .OnEvent('Click', 'ShowHelpEditors')
        
        this.AddButton('xm w80', "&Browse").OnEvent('Click', 'Browse')
        this.AddButton('Default yp w80 x' x - 160 - this.MarginY, "&OK").OnEvent('Click', 'Confirm')
        this.AddButton('yp w80 x' x - 80, "&Cancel").OnEvent('Click', (c, *) => c.Gui.Hide())
        
        this["Eds"].OnEvent("ItemFocus", "EditorSelected")
        this.CmdChanged()
    }
    
    ShowHelpEditors(*) {
        if FileExist(chm := ROOT_DIR '\v2\AutoHotkey.chm')
            Run 'hh.exe "ms-its:' chm '::docs/lib/Edit.htm#Editors"'
        else
            Run 'https://www.autohotkey.com/docs/v2/lib/Edit.htm#Editors'
    }
    
    Browse(*) {
        app := this.FileSelect(3,,, "Apps (*.exe; *.ahk)")
        if app = ""
            return
        this['Cmd'].Value := this.GetAppCmd(app)
        this.CmdChanged()
    }
    
    GetAppCmd(app) {
        SplitPath app,,, &ext
        if ext != "ahk"
            return Format('"{1}" "%l"', app)
        lp := GetLaunchParameters(app, true)
        if !lp.exe
            return ""
        ; Try to use a path that will work if the user installs a new version and removes this one
        ; (rather than invoking the launcher every time the edit verb is executed).
        adaptivePath := RegExReplace(lp.exe.Path, lp.v = 1 ? '\\v1[^\\]*(?=\\[^\\]*$)' : '\\v2\K[^\\]+(?=\\[^\\]*$)')
        trace '![Launcher] ' adaptivePath
        try
            adaptiveExe := GetExeInfo(adaptivePath)
        if !IsSet(adaptiveExe) || VerCompare(adaptiveExe.Version, lp.v) < 0
            adaptivePath := ""
        cmd := Format('"{}"', FileExist(adaptivePath) ? adaptivePath : lp.exe.Path)
        for sw in lp.switches
            cmd .= ' ' sw
        return cmd .= Format(' "{}" "%l"', app)
    }
    
    EditorSelected(lv, index) {
        this['Cmd'].Value := this.Apps[index].cmd
        this.CmdChanged()
    }
    
    CmdChanged(ctrl:=unset, *) {
        if IsSet(ctrl) && n := this['Eds'].GetNext()
            this['Eds'].Modify(n, '-Select')
        cmd := this['Cmd'].Value
        this['OK'].Enabled := cmd != "" && FindExecutable(CommandLineToArgs(cmd)[1]) != ""
    }
    
    SelectEditorByCmd(cmd) {
        if cmd = ""
            return
        for app in this.Apps {
            if app.cmd = cmd {
                this['Eds'].Modify(A_Index, 'Focus Select')
                return
            }
        }
        ; App not in the list, so add it.
        args := CommandLineToArgs(cmd)
        try {
            exe := GetExeInfo(FindExecutable(args.RemoveAt(1)))
            app := {cmd: cmd, exe: exe.Path, name: exe.Description}
            if SubStr(app.name, 1, 10) = "AutoHotkey" && (ahk := ahkArg(args)) {
                ; The app itself appears to be a script, so show the script name.
                app.name := ahk
            }
            this.Apps.Push(app)
            try
                icon := IL_Add(this.IconList, app.exe, IsSet(ahk) && ahk ? 2 : 1)
            catch
                icon := -1
            this['Eds'].Add('Focus Select Icon' icon, app.name)
        }
        
        ahkArg(args) {
            for arg in args {
                if SubStr(arg, 1, 1) = '/'
                    continue
                return SubStr(arg, -4) = '.ahk' ? arg : ''
            }
            return ''
        }
    }
    
    Confirm(*) {
        this.Hide()
        this.OnConfirm(this['Cmd'].Value)
    }
}

class DefaultEditorGui extends EditorSelectionGui {
    __new(scriptToEdit:=unset) {
        cmd := RegRead('HKCR\AutoHotkeyScript\shell\edit\command',, '')
        if InStr(cmd, A_LineFile)
            cmd := ''
        super.__new(cmd)
        if IsSet(scriptToEdit)
            this.ScriptToEdit := scriptToEdit
    }
    
    OnConfirm(cmd) {
        RegWrite(cmd, 'REG_SZ', 'HKCU\Software\Classes\AutoHotkeyScript\shell\edit\command')
        if this.HasProp('ScriptToEdit')
            Run('edit "' this.ScriptToEdit '"')
    }
}

GetEditorApps() {
    apps := []
    apps.byName := Map(), apps.byName.CaseSense := 'off'
    addAssoc(assoc, flag, src) {
        static ASSOCSTR_COMMAND := 1
        static ASSOCSTR_EXECUTABLE := 2
        static ASSOCSTR_FRIENDLYAPPNAME := 4
        try {
            name := AssocQueryString(flag, ASSOCSTR_FRIENDLYAPPNAME, assoc)
            exe := AssocQueryString(flag, ASSOCSTR_EXECUTABLE, assoc)
        }
        if !IsSet(exe) || name ~= 'i)^AutoHotkey|^Ahk2Exe'
            return
        try
            cmd := AssocQueryString(flag, ASSOCSTR_COMMAND, assoc)
        catch
            cmd := '"' exe '" "%l"'
        else if cmd = ""
            return
        if !(InStr(cmd, "%1") || InStr(cmd, "%l"))
            cmd .= ' "%l"'
        if name = "NOTEPAD.EXE"
            name := "Notepad"
        if apps.byName.Has(name)
            return
        app := {cmd: cmd, exe: exe, name: name}
        apps.byName[name] := app
        apps.Push(app)
    }
    addAppExe(app, src) {
        static ASSOCF_INIT_BYEXENAME := 2 ; 0x2
        addAssoc app, ASSOCF_INIT_BYEXENAME, src
    }
    addProgId(app, src) {
        addAssoc app, 0, src
    }
    
    for ext in ["ahk", "txt"] {
        owl := "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\." ext "\OpenWithList"
        mru := RegRead(owl, "MRUList", "")
        Loop Parse mru {
            if app := RegRead(owl, A_LoopField, "")
                addAppExe app, "Explorer\." ext "\OWL"
        }
        Loop Reg "HKCR\." ext "\OpenWithProgIds", "V" {
            addProgId A_LoopRegName, "HKCR\." ext "\OWPI"
        }
        Loop Reg "HKCR\." ext "\OpenWithList", "K" {
            if !InStr(A_LoopRegName, "Ahk2Exe")
                addAppExe A_LoopRegName, "HKCR\." ext "\OWL"
        }
    }
    addAppExe "notepad.exe", "explicit"
    return apps
}

; Return the path of an executable file, if given something that could be executed
; in a shell verb (excluding args).  Although shell verb commands require an exe,
; they do also look in \App Paths\, like ShellExecute, unlike CreateProcess.
FindExecutable(name) {
    if SubStr(name, -4) != ".exe"  ; For odd cases like 'notepad "%1"'
        name .= ".exe"
    if FileExist(name)
        return name
    if InStr(name, "\") || InStr(name, ":")
        return ""
    buf := Buffer(260*2)
    if DllCall("shell32\FindExecutable", "str", name, "ptr", 0, "ptr", buf, "uint") > 32 ; "Returns a value greater than 32 if successful"
        return StrGet(buf)
    static AppPaths := '\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\'
    path := RegRead('HKCU' AppPaths name,, '') || RegRead('HKLM' AppPaths name,, '')
    ; The system permits quotes, and some applications are registered that way.
    return StrReplace(path, '"')
}

AssocQueryString(flags, strtype, assoc) {
    DllCall("shlwapi\AssocQueryStringW", "int", flags, "int", strtype, "wstr", assoc
        , "ptr", 0, "ptr", 0, "uint*", &bufsize := 0, "hresult")
    buf := Buffer(bufsize * 2)
    DllCall("shlwapi\AssocQueryStringW", "int", flags, "int", strtype, "wstr", assoc
        , "ptr", 0, "ptr", buf, "uint*", &bufsize, "hresult")
    return StrGet(buf, "UTF-16")
}

if A_LineFile = A_ScriptFullPath
    DefaultEditorGui.Show(A_Args*)
