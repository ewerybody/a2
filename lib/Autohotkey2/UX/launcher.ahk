; This script is intended for indirect use via commands registered by install.ahk.
; It can also be compiled as a replacement for AutoHotkey.exe, so tools which run
; scripts by executing AutoHotkey.exe can benefit from automatic version selection.
#requires AutoHotkey v2.0

;@Ahk2Exe-SetDescription AutoHotkey Launcher
#SingleInstance Off
#NoTrayIcon

#include inc\identify.ahk
#include inc\launcher-common.ahk
#include inc\ui-base.ahk

if A_ScriptFullPath == A_LineFile || A_LineFile == '*#1' {
    SetWorkingDir A_InitialWorkingDir
    Main
}

Main() {
    switches := []
    while A_Args.length {
        arg := A_Args.RemoveAt(1)
        if SubStr(arg,1,1) != '/' {
            ScriptPath := arg
            break
        }
        nextArgValue() {
            if !A_Args.Length {
                MsgBox "Invalid command line switches; missing value for " arg ".", "AutoHotkey Launcher", "icon!"
                ExitApp 1
            }
            return A_Args.RemoveAt(1)
        }
        switch arg, false {
        case '/RunWith':    ; Launcher-specific
            A_Args.runwith := nextArgValue()
        case '/Launch':     ; Launcher-specific
            A_Args.launch := true
        case '/Which':
            A_Args.which := true
            if trace.Enabled
                trace.DefineProp 'call', {call: (this, s) => OutputDebug(s "`n")} ; Don't use stdout.
        case '/iLib', '/include':
            switches.push(arg)
            switches.push(nextArgValue())
        default:
            switches.push(arg)
        }
        
    }
    if !IsSet(ScriptPath)
        && !FileExist(ScriptPath := A_ScriptDir "\AutoHotkey.ahk")
        && !FileExist(ScriptPath := A_MyDocuments "\AutoHotkey.ahk")
        && !FileExist(ScriptPath := A_ScriptDir "\ui-dash.ahk") {
        ExitApp
    }
    if ScriptPath = '*'
        ExitApp 2 ; FIXME: code would need to be read in and then passed to the real AutoHotkey
    IdentifyAndLaunch ScriptPath, A_Args, switches
}

GetLaunchParameters(ScriptPath, interactive:=false) {
    code := FileRead(ScriptPath, 'UTF-8')
    require := prefer := rule := exe := ""
    if RegExMatch(code, 'im)^[ `t]*#Requires[ `t]+AutoHotkey[ `t]+([^;`r`n]*?)[ `t]*(?:;[ `t]*prefer[ `t]+([^;`r`n\.]+))?(?:$|;)', &m) {
        trace "![Launcher] " m.0
        require := RegExReplace(m.1, '[^\s,]\K\s+(?!$)', ",")
        prefer := RegExReplace(m.2, '[^\s,]\K\s+(?!$)', ",")
        rule := "#Requires"
    }
    else if ConfigRead('Launcher', 'Identify', true) {
        i := IdentifyBySyntax(code)
        trace "![Launcher] syntax says version " (i.v || "unknown") " -- " i.r
        if i.v
            require := String(i.v)
        rule := i.r
        if rule = "error"
            MsgBox "Syntax detection has failed due to an error in the launcher.`n`n" Type(i.err) ": " i.err.Message " " i.err.Extra "`n`n"
                . "Character index " i.pos "`n" SubStr(code, i.pos, 50) "`n...`n`n"
                . "Please report this on the forums, with sample code that triggers the error.", "AutoHotkey Launcher", "icon!"
    }
    else {
        trace "![Launcher] version unknown - syntax-checking is disabled"
    }
    if !(hasv := RegExMatch(require, '(^|,)\s*(?!(32|64)-bit)[<>=]*v?\d')) {
        ; No version specified or detected
        if hasv := v := ConfigRead('Launcher', 'Fallback', "") {
            require .= (require=''?'':',') v
            trace "![Launcher] using fallback version " v
        }
    }
    v := GetVersionToInstall(require) ; Currently used for multiple purposes
    if !hasv
        exe := interactive ? PromptMajorVersion(ScriptPath, require, prefer) : ""
    else
        if !exe := GetRequiredOrPreferredExe(require, prefer)
            if interactive {
                if v && !LocateExeByVersion(v, '')
                    exe := TryToInstallVersion(v, rule, ScriptPath, require, prefer)
                else
                    RequirementNotMetMsgBox require, ScriptPath
            }
    lp := {exe: exe, id: exe ? GetMajor(exe.Version) : GetLikelyMajor(require), v: v, switches: []}
    if exe {
        if GetMajor(exe.Version) = 1 && ConfigRead('Launcher\v1', 'UTF8', false)
            lp.switches.Push('/CP65001')
    }
    return lp
}

ParseRequiresVersion(s) {
    return RegExMatch(s, 'i)^(?!(?:32|64)-bit$)(?<op>[<>=]*)v?(?<version>(?<major>\d+)\b\S*)', &m) ? m : 0
}

GetLikelyMajor(r) {
    if IsNumber(r)
        return Integer(r)
    ; Usually there would be either a version number with no operator
    ; or a range where the lower and upper bound have the same major.
    Loop Parse r, ",", " `t"
        if (m := ParseRequiresVersion(A_LoopField)) && m.op != '<'
            return m.major
    return ''
}

GetVersionToInstall(r) {
    ; TryToInstallVersion currently only supports the latest bug-fix release,
    ; so don't try to install if there's a complex version requirement.
    if IsNumber(r)
        return r
    v := ""
    Loop Parse r, ",", " `t" {
        if (m := ParseRequiresVersion(A_LoopField)) {
            if m.op
                return ''
            v := m.version
        }
    }
    return v
}

IdentifyAndLaunch(ScriptPath, args, switches) {
    lp := GetLaunchParameters(ScriptPath, !(whichMode := args.HasProp('which')))
    if whichMode {
        try FileAppend(lp.v "`n"
            (lp.exe ? lp.exe.Path : "") "`n"
            (lp.switches.Length ? lp.switches[1] : "") "`n", '*', 'UTF-8-RAW')
        ExitApp lp.id
    }
    if !lp.exe
        ExitApp 2
    switches.Push(lp.switches*)
    ExitApp LaunchScript(lp.exe.Path, ScriptPath, args, switches)
}

TryToInstallVersion(v, r, ScriptPath, require, prefer) {
    ; This is currently designed only for downloading the latest bug-fix of a given minor version.
    SplitPath ScriptPath, &name
    m := ' script you are trying to run requires AutoHotkey v' v ', which is not installed.'
    m := !(r && r != '#Requires') ? 'The' m '`n`nScript:`t' name : 'It looks like the' m '`nIf the version has been misidentified, please add a #Requires directive to your script file.`n`nScript:`t' name '`nRule:`t' r
    if downloadable := IsNumber(v) || VerCompare(v, '1.1.24.02') >= 0 {
        ; Get current version compatible with v.
        bv := v = 1 ? '1.1' : IsInteger(v) ? v '.0' : RegExReplace(v, '^\d+(?:\.\d+)?\b\K.*')
        req := ComObject('Msxml2.XMLHTTP')
        req.open('GET', Format('https://www.autohotkey.com/download/{}/version.txt', bv), false)
        try req.send()
        if req.status = 200 && RegExMatch(cv := req.responseText, '^\d+\.[\w\+\-\.]+$') && VerCompare(cv, v) >= 0
            m .= '`n`nWe can try to download and install AutoHotkey v' cv ' for you, while retaining the ability to use the versions already installed.`n`nDownload and install AutoHotkey v' cv '?'
        else
            downloadable := false
    }
    if downloadable && !A_IsAdmin && RegRead('HKLM\SOFTWARE\AutoHotkey', 'InstallDir', "") = ROOT_DIR
        SetTimer(() => (
            WinExist('ahk_class #32770 ahk_pid ' ProcessExist()) &&
            SendMessage(0x160C,, true, 'Button1') ; BCM_SETSHIELD := 0x160C
        ), -25)
    if MsgBox(m, 'AutoHotkey', downloadable ? 'Iconi y/n' : 'Icon!') != 'yes'
        return false
    if RunWait(Format('"{}" /script "{}\install-version.ahk" "{}"', A_AhkPath, A_ScriptDir, cv)) != 0
        return false
    return exe := GetRequiredOrPreferredExe(require, prefer)
}

RequirementNotMetMsgBox(require, ScriptPath) {
    SplitPath ScriptPath, &name
    MsgBox 'Unable to locate the appropriate interpreter to run this script.`n`nScript:`t' name '`nRequires: ' StrReplace(require, ',', ' '), 'AutoHotkey', 'Icon!'
}

GetRequiredOrPreferredExe(require, prefer:='') {
    if A_Args.HasProp('runwith')
        prefer := A_Args.runwith ',' prefer
    return LocateExeByVersion(require, Trim(prefer, ','))
}

LocateExeByVersion(require, prefer:='!UIA, 64, !ANSI') {
    trace '![Launcher] locating exe: require ' require (prefer='' ? '' : '; prefer ' prefer)
    best := '', bestscore := 0, cPrefMap := Map()
    for ,f in GetUsableAutoHotkeyExes() {
        try {
            ; Check requirements first
            fMajor := GetMajor(f.Version)
            Loop Parse require, ",", " " {
                if A_LoopField = ""
                    continue
                if m := ParseRequiresVersion(A_LoopField) {
                    if !VerCompare(f.Version, (m.op ? '' : '>=') A_LoopField) {
                        ; trace '![Launcher] ' f.Version ' ' (m.op ? '' : '>=') A_LoopField ' = false'
                        continue 2
                    }
                    if !m.op && fMajor > m.major { ; No operator implies it must be same major version
                        ; trace '![Launcher] major ' f.Version ' > ' m.version
                        continue 2
                    }
                }
                else if !matchPref(f.Description, A_LoopField) {
                    ; trace '![Launcher] no match for "' A_LoopField '" in ' f.Description
                    continue 2
                }
            }
            ; Determine additional user preferences based on major version
            if !(cPref := cPrefMap.Get(fMajor, 0)) {
                section := 'Launcher\v' fMajor
                cPref := ConfigRead(section, 'Version', "")
                cPref := {
                    V: cPref ? '=' cPref ',' : '<0,',
                    D: ',' (ConfigRead(section, 'Build', (A_Is64bitOS ? "64," : "") "!ANSI"))
                    .  ',' (ConfigRead(section, 'UIA', false) ? 'UIA' : '!UIA')
                }
                cPrefMap.Set(fMajor, cPref)
            }
            ; Calculate preference score
            fscore := 0
            Loop Parse cPref.V prefer cPref.D, ",", " " {
                if A_LoopField = ""
                    continue
                fscore <<= 1
                if !(A_LoopField ~= '^[<>=]' ? VerCompare(f.Version, A_LoopField)
                    : matchPref(f.Description, A_LoopField))
                    continue
                fscore |= 1
            }
            ; trace '![Launcher] ' fscore ' v' f.Version ' ' f.Path
            ; Prefer later version if all else matches.  If version also matches, prefer later files,
            ; as enumeration order is generally AutoHotkey.exe, ..A32.exe, ..U32.exe, ..U64.exe.
            if bestscore < fscore
                || bestscore = fscore && VerCompare(f.Version, best.Version) >= 0
                bestscore := fscore, best := f
        }
        catch as e {
            trace "-[Launcher] " type(e) " checking file " A_LoopFileName ": " e.message
            trace "-[Launcher] " e.file ":" e.line
        }
    }
    return best
    matchPref(desc, pref) => SubStr(pref,1,1) != "!" ? InStr(desc, pref) : !InStr(desc, SubStr(pref,2))
}

PromptMajorVersion(ScriptPath, require:='', prefer:='') {
    majors := Map()
    Loop 2
        if f := GetRequiredOrPreferredExe(A_Index ',' require, prefer)
            majors[A_Index] := f
    switch majors.Count {
    case 1:
        for , f in majors
            return f
    case 0:
        trace '-[Launcher] Failed to locate any interpreters; fallback to launcher'
        return {Path: A_AhkPath, Version: A_AhkVersion}
    }
    files := []
    for , f in majors
        files.Push(f)
    prompt := VersionSelectGui(ScriptPath, files)
    prompt.Show
    WinWaitClose prompt
    if !prompt.HasProp('selection') {
        trace '[Launcher] No version selected from menu'
        ExitApp
    }
    return prompt.selection
}

class Handle {
    __new(ptr:=0) => this.ptr := ptr
    __delete() => DllCall("CloseHandle", "ptr", this)
}

LaunchScript(exe, ahk, args:="", switches:="", encoding:="UTF-8") {
    ; Pass our own stdin/stdout handles (if any) to the child process.
    hStdIn  := DllCall("GetStdHandle", "uint", -10, "ptr")
    hStdOut := DllCall("GetStdHandle", "uint", -11, "ptr")
    hStdErr := DllCall("GetStdHandle", "uint", -12, "ptr")
    
    ; Build command line to execute.
    makeArgs(args) {
        r := ''
        for arg in args is object ? args : [args]
            r .= ' ' (arg ~= '\s' ? '"' arg '"' : arg)
        return r
    }
    switches := makeArgs(switches)
    cmd := Format('"{1}"{2} "{3}"{4}', exe, switches, ahk, makeArgs(args))
    trace '>[Launcher] ' cmd
    
    ; For RunWait, stdout redirection, /validate, etc. to have the best chance of working,
    ; let the launcher exit early only if it can detect that it was executed from Explorer
    ; or the parent process appears to have exited already (or if the caller passed /launch).
    waitClose := !args.HasProp('launch')
    hParent := 0
    if IsSet(ProcessGetParent) {
        try {
            ; (PROCESS_QUERY_LIMITED_INFORMATION := 0x1000) | (SYNCHRONIZE := 0x100000)
            if hParent := DllCall("OpenProcess", "uint", 0x101000, "int", false
                , "uint", parentPid := ProcessGetParent(), "ptr")
                hParent := Handle(hParent)
            if !hParent || (parentName := ProcessGetName(parentPid)) = "explorer.exe"
                waitClose := false
        }
        catch as e
            trace '![Launcher] Failure checking parent process: ' e.Message
    }

    try {
        proc := RunWithHandles(cmd, {in: hStdIn, out: hStdOut, err: hStdErr})
    }
    catch OSError as e {
        if e.Number != 740 ; ERROR_ELEVATION_REQUIRED
            throw
        trace '![Launcher] elevation required; handles will not be redirected'
        cmd := RegExReplace(cmd, ' /ErrorStdOut(?:=\S*)?')
        Run cmd
        ExitApp
    }
    
    ; When the /launch switch is used, return the process ID as the launcher's exit code.
    if args.HasProp('launch')
        return proc.pid
    
    if waitClose {
        ; Wait for either the child process or our parent process (if determined) to terminate.
        NumPut 'ptr', proc.hProcess.ptr, 'ptr', hParent ? hParent.ptr : 0, waitHandles := Buffer(A_PtrSize*2)
        loop {
            Sleep -1
            waitResult := DllCall("MsgWaitForMultipleObjects", "uint", 1 + (hParent != 0), "ptr", waitHandles, "int", 0, "uint", -1, "uint", 0x04FF)
        } until waitResult = 0 || waitResult = 1
    }
    
    DllCall("GetExitCodeProcess", "ptr", proc.hProcess, "uint*", &exitCode:=0)
    if trace.Enabled {
        ; We have to return something numeric for ExitApp, so currently exitCode is left as 259
        ; if the process is still running.
        if exitCode = 259 && DllCall("WaitForSingleObject", "ptr", proc.hProcess, "uint", 0) = 258 { ; STILL_ACTIVE = 259, WAIT_TIMEOUT = 258
            if !(hParent ?? 1) || (waitResult ?? -1) = 1
                trace '>[Launcher] Process launched; now exiting because parent process has terminated.'
            else if (parentName ?? "") = "explorer.exe"
                trace '>[Launcher] Process launched; now exiting because parent is explorer.exe.'
            else
                trace '>[Launcher] Process launched; launcher exiting early.'
        }
        else        
            trace '>[Launcher] Exit code: ' exitCode
    }
    
    return exitCode
}

RunWithHandles(cmd, handles, workingDir:="") {
    static STARTUPINFO_SIZE := A_PtrSize=8 ? 104 : 68
        , STARTUPINFO_dwFlags := A_PtrSize=8 ? 60 : 44
        , STARTUPINFO_hStdInput := A_PtrSize=8 ? 80 : 56
        , STARTF_USESTDHANDLES := 0x100
        , PROCESS_INFORMATION_SIZE := A_PtrSize=8 ? 24 : 16
    HandleValue(p) => HasProp(handles, p) && (IsInteger(h := handles.%p%) ? h : h.Ptr)
    si := Buffer(STARTUPINFO_SIZE, 0)
    NumPut("uint", STARTUPINFO_SIZE, si)
    NumPut("uint", STARTF_USESTDHANDLES, si, STARTUPINFO_dwFlags)
    NumPut("ptr", HandleValue("in")
         , "ptr", HandleValue("out")
         , "ptr", HandleValue("err")
         , si, STARTUPINFO_hStdInput)
    pi := Buffer(PROCESS_INFORMATION_SIZE)
    if !DllCall("CreateProcess", "ptr", 0, "str", cmd, "ptr", 0, "int", 0, "int", true
                , "int", 0x08000000, "int", 0, "ptr", workingDir ? StrPtr(workingDir) : 0
                , "ptr", si, "ptr", pi)
        throw OSError(, -1, cmd)
    return { hProcess: Handle(NumGet(pi, 0, "ptr"))
           , hThread: Handle(NumGet(pi, A_PtrSize, "ptr"))
           , pid: NumGet(pi, A_PtrSize*2, "uint") }
}

class VersionSelectGui extends AutoHotkeyUxGui {
    __new(script, files) {
        SplitPath script, &scriptName
        super.__new("Run " scriptName " with", '-MinimizeBox')
        DllCall('uxtheme\SetWindowThemeAttribute', 'ptr', this.hwnd, 'int', 1 ; WTA_NONCLIENT
            , 'int64*', 2 | (2<<32), 'int', 8) ; WTNCA_NODRAWICON=2
        lv := this.AddListMenu('vList LV0x40 w200', ["Version"])
        lv.OnEvent('Focus', 'Focused')
        lv.OnEvent('LoseFocus', 'Focused')
        lv.OnEvent('Click', 'Confirm')
        il := IL_Create(,, false)
        lv.SetImageList(il, 0)
        for f in this.files := files {
            lv.Add('Icon' IL_Add(il, f.Path), f.Version " " StrReplace(f.Description, "AutoHotkey "))
        }
        lv.AutoSize(8)
        lv.GetPos(&x, &y, &w, &h)
        this.Show('AutoSize Hide')
        this.AddButton('Default Hidden', "Confirm").OnEvent('Click', 'Confirm')
    }
    
    Confirm(*) {
        if !(i := this['List'].GetNext())
            return
        this.selection := this.files[i]
        this.Hide()
    }
    
    Focused(ctrl, *) {
        OnMessage(0x101, keyup, ctrl.Focused)
        static keyup(wParam, lParam, nmsg, hwnd) {
            local this := GuiFromHwnd(hwnd, true)
            if IsDigit(GetKeyName(Format("vk{:x}", wParam))) && this['List'].GetNext() {
                this.Confirm()
                return true
            }
        }
    }
}
