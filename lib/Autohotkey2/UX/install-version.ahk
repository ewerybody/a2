; Run this script to download and install an additional AutoHotkey version.
; Specify the version as a single command line parameter.  If omitted or
; incomplete like "1.1" or "2.0", the latest version will be downloaded.
#requires AutoHotkey v2.0

#include install.ahk

A_ScriptName := "AutoHotkey"

InstallAutoHotkey A_Args.Length ? A_Args[1] : '1.1'

InstallAutoHotkey(version) {
    abort(message, extra?) {
        if IsSet(extra)
            message .= "`n`nSpecifically: " SubStr(extra, 1, 100)
        MsgBox message,, "Iconx"
        ExitApp
    }
    
    ; Determine base version, for download directory
    baseVersion := RegExReplace(version, '^\d+(?:\.\d+)?\b\K.*')
    if IsInteger(baseVersion)
        baseVersion .= baseVersion = '1' ? '.1' : '.0'
    else if !IsNumber(baseVersion)
        abort "Invalid version.", version

    ; If version number is not exact, try to determine the latest compatible version
    if IsNumber(version) {
        url := Format('https://www.autohotkey.com/download/{}/version.txt', baseVersion)
        req := ComObject('Msxml2.XMLHTTP')
        req.open('GET', url, false)
        req.send()
        if req.status != 200
            throw Error(req.status ' - ' req.statusText, -1)
        currentVersion := req.responseText
        if VerCompare(currentVersion, baseVersion) < 0 || VerCompare(currentVersion, Round(baseVersion + 1)) >= 0
            abort "An error occurred while trying to identify the latest available version. The downloaded version.txt was invalid.", currentVersion
        version := currentVersion
    }

    ; Only versions for which a zip is available are supported by this script.
    ; 1.1.00.00 - 1.1.22.06 have no downloads available at the time of writing.
    ; 1.1.22.07 - 1.1.24.01 have one zip per exe.
    if VerCompare(version, '1.1') >= 0 && VerCompare(version, '1.1.24.02') < 0
        abort "This version cannot be installed automatically.", version

    inst := Installation()
    inst.ResolveInstallDir()

    if A_Args.Length < 2 && !A_IsAdmin && !inst.UserInstall {
        ExitApp RunWait(Format('*RunAs "{1}" /force /script "{2}" {3} /Y', A_AhkPath, A_ScriptFullPath, version))
    }

    zipName := VerCompare(version, '1.1.24.02') < 0
        ? 'AutoHotkey' StrReplace(version, '.') '.zip'
        : 'AutoHotkey_' version '.zip'
    url := Format('https://www.autohotkey.com/download/{}/{}', baseVersion, zipName)

    try {
        tempDir := inst.InstallDir '\.staging' ; Avoid A_Temp for security reasons
        try {
            DirCreate tempDir
            SetWorkingDir tempDir
        }
        catch OSError as e
            abort "An error occured while preparing the temporary directory.", e.Message

        TrayTip "Downloading AutoHotkey v" version, "AutoHotkey"
        try
            Download url, tempDir '\' zipName
        catch
            abort "Download failed.`n`nURL: " url

        TrayTip "Installing AutoHotkey v" version, "AutoHotkey"
        inst.SourceDir := tempDir '\v' version
        try
            DirCopy tempDir '\' zipName, inst.SourceDir, true
        catch
            abort "Extraction failed."
        finally
        try
            FileDelete zipName
        catch
            MsgBox 'Unable to delete temporary file "' tempDir '\' zipName '".',, "Icon!"
        
        try localUX := inst.Hashes['UX\install.ahk']
        catch
            localUX := {Version: ''}
        try {
            if VerCompare(localUX.Version, version) < 0
                && FileExist(inst.SourceDir '\UX\install.ahk')
                && FileExist(inst.SourceDir '\AutoHotkey32.exe') {
                Run Format('"{1}\AutoHotkey32.exe" UX\install.ahk /to "{2}"', inst.SourceDir, inst.InstallDir), inst.SourceDir
                ExitApp
            }
            else
                inst.InstallExtraVersion
        }
        catch as e
            abort "An error occurred during installation.", e.Message
    }
    finally {
        try DirDelete tempDir '\v' version, true
        try DirDelete tempDir
    }

    TrayTip
    MsgBox "AutoHotkey v" version " is now installed."
}
