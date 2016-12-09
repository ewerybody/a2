TriggerFromOtherInstance(wParam, lParam)
{
    if (lParam = 0) ;0 = Single trigger from something else than context menus
    {
        ExecuteTrigger(wParam)
    } else if (lParam = 1) ;1 = Trigger from context menu
    {
        ; Read list of selected files written by shell extension
        if (FileExist(A_Temp "\7plus\files.txt"))
            FileRead, files, % "*t " A_Temp "\7plus\files.txt"
        FileDelete, % A_Temp "\7plus\files.txt"
        ; if it failed (because static context menu is used), try to get it from explorer window
        files := files ? files : Navigation.GetSelectedFilepaths()

        ; TODO
    }
}

ProcessCommandLineParameters()
{
    global
    local Count, hwnd, i, Parameter, Parameters
    DetectHiddenWindows, On

    ; InitWorkerThread() ;This processes all cases where 7plus acts as a worker thread for another 7plus instance
    FileRead, hwnd, %A_Temp%\a2\hwnd.txt ;if existing, hwnd.txt contains the window handle of another running instance
    Parameters := []
    Loop %0%
        Parameters[A_Index] := %A_Index%

    ; if a path is supplied as first parameter, set explorer directory to this path and exit
    if (InStr(FileExist(Parameters[1]), "D"))
    {
        Msgbox Navigation.SetPath(Parameters[1])
        ExitApp
    }
    for i, Parameter in Parameters
    {
        ; TODO: Change this format to "-id Number" for compatibility with Explorer Button trigger? (See EventSystem_Startup())
        ; Generic event trigger, send to running instance
        if (InStr(Parameter, "-id") = 1)
        {
            if (WinExist("ahk_id " hwnd))
            {
                Parameter := SubStr(Parameter, 5) ;-ID:Value
                SendMessage, 55555, %Parameter%, 0, ,ahk_id %hwnd%
                ExitApp
            }
        }
        ; Trigger from legacy context menu mechanism (used for My Computer menu), send to running instance
        else if (InStr(Parameter,"-ContextID") = 1)
        {
            if (WinExist("ahk_id " hwnd))
            {
                Parameter := SubStr(Parameter, 12) ; -ContextID:Value
                SendMessage, 55555, %Parameter%, 1, ,ahk_id %hwnd%
                ExitApp
            }
        }
    }
    if (hwnd && WinGetClass("ahk_id " hwnd ) = "AutoHotkey")
        ExitApp
}

ReleaseInstance()
{
    global
    WriteDebug("OnExit()")

    msgbox % A_ExitReason

    OnMessage(0x218, "")  ; WM_POWERBROADCAST
    OnMessage(0x031D, "") ; OnClipboardChange
    ; OnMessage(ApplicationState.ShellHookMessage, "")
    ; DllCall("DeregisterShellHookWindow", "Ptr", A_ScriptHwnd)

    if (A_ExitReason == "Reload") {
        deleteHwnd := true
    }

    if (deleteHwnd) {
        msgbox % "delete"
        FileRemoveDir, %A_Temp%\a2, 1
    }
}

RegisterTrigger(cmd)
{
    id := FindAvailableTriggerID()
    Triggers[id] := cmd
    return id
}

FindAvailableTriggerID()
{
    Loop, 9999
    {
        if (!GetTrigger(A_Index))
            return A_Index
    }
    return false
}

GetTrigger(id)
{
    for _id, cmd in Triggers
        if (id == _id)
            return id
    return false
}

ExecuteTrigger(id)
{
    for _id, cmd in Triggers
        if (id == _id)
            %cmd%()
}
