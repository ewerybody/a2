paste( byref inputString, sleepTime=50 ){
    SavedClipboard := ClipboardAll
    Clipboard =
    Sleep, %sleepTime%
    Clipboard := inputString
    ClipWait, 1
    Send, {Ctrl down}^v{Ctrl up}
    Clipboard := SavedClipboard
}

; looks up the items of an array object
; returns index of search string if found
; returns 0 otherwise
inArray(byref search, byref array) {
    ;for i, value in array {
    Loop % array.MaxIndex() {
        if (search == array[A_Index])
            Return A_Index
    }
    Return 0
}

/**
 * Helper Function
 *     Returns a free identifier for a GUI
 *     v0.81 by majkinetor  Licenced under BSD <http://creativecommons.org/licenses/BSD/>
 *
 * @sample
 *     GetFreeGuiNum(0)         ; returns the first integer that is not used by a GUI
 * @sample
 *     GetFreeGuiNum(10, "Foo") ; returns "Foo10" or the next higher integer that is not used by a GUI
 *
 * @param   integer     start   Number from where to start counting up
 * @param   string      prefix  String to help the GUI identifier to be unique
 * @return  string
 */
GetFreeGuiNum(start, prefix = ""){
    loop
    {
        Gui %prefix%%start%:+LastFoundExist
        IfWinNotExist
            return prefix start
        start++
        if (start = 100)
            return 0
    }
    return 0
}

/**
 * Helper Function
 *     Retrieves the coordinates of a window's client area
 *
 * @sample
 *     GetClientRect(WinExist("A"))
 *
 * @param   HWND    hwnd     Handler of the window to be found
 * @return  object
 */
; Gets client area of a window
GetClientRect(hwnd)
{
    VarSetCapacity(rc, 16)
    result := DllCall("GetClientRect", "PTR", hwnd, "PTR", &rc, "UINT")
    return {x : NumGet(rc, 0, "int"), y : NumGet(rc, 4, "int"), w : NumGet(rc, 8, "int"), h : NumGet(rc, 12, "int")}
}

/**
 * Helper Function
 *     Clamp a value
 *
 * @sample
 *     clamp(3, 10, 20) ; return 10
 *
 * @param   integer     value   value to be compared
 * @param   integer     min     minumum value to be returned
 * @param   integer     max     maximum value to be returned
 * @return  integer
 */
; Clamps a value
Clamp(value, min, max)
{
    if (value < min)
        value := min
    else if (value > max)
        value := max
    return value
}

/**
 * Helper Function
 *     Returns the MonitorID where the specified window is located on
 *     By shnywong
 *
 * @sample
 *     GetMonitorIndexFromWindow(WinExist("A"))
 *
 * @param   HWND     hwnd     Handler of the window to be found
 * @return  integer
 *
 * @docu    https://autohotkey.com/board/topic/69464-how-to-determine-a-window-is-in-which-monitor/#entry440355
 */
GetMonitorIndexFromWindow(hwnd)
{
    ; Starts with 1.
    monitorIndex := 1

    VarSetCapacity(monitorInfo, 40)
    NumPut(40, monitorInfo)

    if (monitorHandle := DllCall("MonitorFromWindow", "uint", hwnd, "uint", 0x2))
        && DllCall("GetMonitorInfo", "uint", monitorHandle, "uint", &monitorInfo)
    {
        monitorLeft   := NumGet(monitorInfo,  4, "Int")
        monitorTop    := NumGet(monitorInfo,  8, "Int")
        monitorRight  := NumGet(monitorInfo, 12, "Int")
        monitorBottom := NumGet(monitorInfo, 16, "Int")
        workLeft      := NumGet(monitorInfo, 20, "Int")
        workTop       := NumGet(monitorInfo, 24, "Int")
        workRight     := NumGet(monitorInfo, 28, "Int")
        workBottom    := NumGet(monitorInfo, 32, "Int")
        isPrimary     := NumGet(monitorInfo, 36, "Int") & 1

        SysGet, monitorCount, MonitorCount

        Loop, %monitorCount%
        {
            SysGet, tempMon, Monitor, %A_Index%

            ; Compare location to determine the monitor index.
            if ((monitorLeft = tempMonLeft) and (monitorTop = tempMonTop)
                and (monitorRight = tempMonRight) and (monitorBottom = tempMonBottom))
            {
                monitorIndex := A_Index
                break
            }
        }
    }

    return %monitorIndex%
}

GetMonitorIndexFromCoords(coords)
{
    n := StrSplit(coords, ",")
    nX := n[1]
    nY := n[2]
    nW := n[3]
    nH := n[4]

    centerX := nX + nW/2
    centerY := nY + nH/2

    ; Starts with 1.
    monitorIndex := 1
    SysGet, monitorCount, MonitorCount
    Loop, %monitorCount%
    {
        SysGet, tempMon, Monitor, %A_Index%

        ; Compare location to determine the monitor index.
        If ((centerX >= tempMonLeft) AND (centerX <= tempMonRight) AND (centerY >= tempMonTop) AND (centerY <= tempMonBottom))
            return A_Index
    }

    return monitorIndex
}

/**
 * Helper Function
 *     Evaluate if the input is a number
 *
 * @sample
 *     IsNumertic(4) ;true
 * @sample
 *     IsNumertic("foo") ;false
 *
 * @param   any     InputObject     Content to be evaluated
 * @return  bool
 */
IsNumeric(InputObject)
{
   If InputObject is number
      Return 1
   Return 0
}

/**
 * Helper Function
 *     Watches a directory/file for file changes
 *     By HotKeyIt
 *
 * @sample
 *     WatchDirectory("C:\temp\*|.txt\|.ini\|\a","ReportChanges")    ; executes ReportChanges(oldName, NewName) {} when a files changes
 * @sample
 *     WatchDirectory("C:\Temp","ReportFunction",0x1|0x2|0x8|0x40)   ; same as above but only for changes:
 *                                                                         FILE_NOTIFY_CHANGE_FILE_NAME,
 *                                                                         FILE_NOTIFY_CHANGE_DIR_NAME,
 *                                                                         FILE_NOTIFY_CHANGE_SIZE,
 *                                                                         FILE_NOTIFY_CHANGE_CREATION
 *
 * @param   *       p*       Specify a valid path to watch for changes in
 * @return  callback
 *
 * @warning
 *     BEFORE EXITING, THE WATCHERS SHOULD BE STOPPED.
 *     This can be done in _OnExit_ by calling the function with empty parameter
 *
 * @docu   https://github.com/HotKeyIt/WatchDirectory/
 * @docu   https://autohotkey.com/board/topic/60125-ahk-lv2-watchdirectory-report-directory-changes/
 */
#include lib\ahklib\_Struct.ahk
WatchDirectory(p*){
    ;Structures
    static FILE_NOTIFY_INFORMATION:="DWORD NextEntryOffset,DWORD Action,DWORD FileNameLength,WCHAR FileName[1]"
    static OVERLAPPED:="ULONG_PTR Internal,ULONG_PTR InternalHigh,{struct{DWORD offset,DWORD offsetHigh},PVOID Pointer},HANDLE hEvent"
    ;Variables
    static running,sizeof_FNI=65536,temp1:=VarSetCapacity(nReadLen,8),WatchDirectory:=RegisterCallback("WatchDirectory","F",0,0)
    static timer,ReportToFunction,LP,temp2:=VarSetCapacity(LP,(260)*(A_PtrSize/2),0)
    static @:=Object(),reconnect:=Object(),#:=Object(),DirEvents,StringToRegEx="\\\|.\.|+\+|[\[|{\{|(\(|)\)|^\^|$\$|?\.?|*.*"
    ;ReadDirectoryChanges related
    static FILE_NOTIFY_CHANGE_FILE_NAME=0x1,FILE_NOTIFY_CHANGE_DIR_NAME=0x2,FILE_NOTIFY_CHANGE_ATTRIBUTES=0x4
          ,FILE_NOTIFY_CHANGE_SIZE=0x8,FILE_NOTIFY_CHANGE_LAST_WRITE=0x10,FILE_NOTIFY_CHANGE_CREATION=0x40
          ,FILE_NOTIFY_CHANGE_SECURITY=0x100
    static FILE_ACTION_ADDED=1,FILE_ACTION_REMOVED=2,FILE_ACTION_MODIFIED=3
          ,FILE_ACTION_RENAMED_OLD_NAME=4,FILE_ACTION_RENAMED_NEW_NAME=5
    static OPEN_EXISTING=3,FILE_FLAG_BACKUP_SEMANTICS=0x2000000,FILE_FLAG_OVERLAPPED=0x40000000
          ,FILE_SHARE_DELETE=4,FILE_SHARE_WRITE=2,FILE_SHARE_READ=1,FILE_LIST_DIRECTORY=1
    If p.MaxIndex(){
       If (p.MaxIndex()=1 && p.1=""){
          for i,folder in #
             DllCall("CloseHandle","Uint",@[folder].hD),DllCall("CloseHandle","Uint",@[folder].O.hEvent)
             ,@.Remove(folder)
          #:=Object()
          DirEvents:=new _Struct("HANDLE[1000]")
          DllCall("KillTimer","Uint",0,"Uint",timer)
          timer=
          Return 0
       } else {
          if p.2
             ReportToFunction:=p.2
          If !IsFunc(ReportToFunction)
             Return -1 ;DllCall("MessageBox","Uint",0,"Str","Function " ReportToFunction " does not exist","Str","Error Missing Function","UInt",0)
          RegExMatch(p.1,"^([^/\*\?<>\|""]+)(\*)?(\|.+)?$",dir)
          if (SubStr(dir1,0)="\")
             StringTrimRight,dir1,dir1,1
          StringTrimLeft,dir3,dir3,1
          If (p.MaxIndex()=2 && p.2=""){
             for i,folder in #
                If (dir1=SubStr(folder,1,StrLen(folder)-1))
                   Return 0 ,DirEvents[i]:=DirEvents[#.MaxIndex()],DirEvents[#.MaxIndex()]:=0
                            @.Remove(folder),#[i]:=#[#.MaxIndex()],#.Remove(i)
             Return 0
          }
       }
       if !InStr(FileExist(dir1),"D")
          Return -1 ;DllCall("MessageBox","Uint",0,"Str","Folder " dir1 " does not exist","Str","Error Missing File","UInt",0)
       for i,folder in #
       {
          If (dir1=SubStr(folder,1,StrLen(folder)-1) || (InStr(dir1,folder) && @[folder].sD))
                Return 0
          else if (InStr(SubStr(folder,1,StrLen(folder)-1),dir1 "\") && dir2){ ;replace watch
             DllCall("CloseHandle","Uint",@[folder].hD),DllCall("CloseHandle","Uint",@[folder].O.hEvent),reset:=i
          }
       }
       LP:=SubStr(LP,1,DllCall("GetLongPathName","Str",dir1,"Uint",&LP,"Uint",VarSetCapacity(LP))) "\"
       If !(reset && @[reset]:=LP)
          #.Insert(LP)
       @[LP,"dir"]:=LP
       @[LP].hD:=DllCall("CreateFile","Str",StrLen(LP)=3?SubStr(LP,1,2):LP,"UInt",0x1,"UInt",0x1|0x2|0x4
                   ,"UInt",0,"UInt",0x3,"UInt",0x2000000|0x40000000,"UInt",0)
       @[LP].sD:=(dir2=""?0:1)

       Loop,Parse,StringToRegEx,|
          StringReplace,dir3,dir3,% SubStr(A_LoopField,1,1),% SubStr(A_LoopField,2),A
       StringReplace,dir3,dir3,%A_Space%,\s,A
       Loop,Parse,dir3,|
       {
          If A_Index=1
             dir3=
          pre:=(SubStr(A_LoopField,1,2)="\\"?2:0)
          succ:=(SubStr(A_LoopField,-1)="\\"?2:0)
          dir3.=(dir3?"|":"") (pre?"\\\K":"")
                . SubStr(A_LoopField,1+pre,StrLen(A_LoopField)-pre-succ)
                . ((!succ && !InStr(SubStr(A_LoopField,1+pre,StrLen(A_LoopField)-pre-succ),"\"))?"[^\\]*$":"") (succ?"$":"")
       }
       @[LP].FLT:="i)" dir3
       @[LP].FUNC:=ReportToFunction
       @[LP].CNG:=(p.3?p.3:(0x1|0x2|0x4|0x8|0x10|0x40|0x100))
       If !reset {
          @[LP].SetCapacity("pFNI",sizeof_FNI)
          @[LP].FNI:=new _Struct(FILE_NOTIFY_INFORMATION,@[LP].GetAddress("pFNI"))
          @[LP].O:=new _Struct(OVERLAPPED)
       }
       @[LP].O.hEvent:=DllCall("CreateEvent","Uint",0,"Int",1,"Int",0,"UInt",0)
       If (!DirEvents)
          DirEvents:=new _Struct("HANDLE[1000]")
       DirEvents[reset?reset:#.MaxIndex()]:=@[LP].O.hEvent
       DllCall("ReadDirectoryChangesW","UInt",@[LP].hD,"UInt",@[LP].FNI[""],"UInt",sizeof_FNI
                ,"Int",@[LP].sD,"UInt",@[LP].CNG,"UInt",0,"UInt",@[LP].O[""],"UInt",0)
       Return timer:=DllCall("SetTimer","Uint",0,"UInt",timer,"Uint",50,"UInt",WatchDirectory)
    } else {
       Sleep, 0
       for LP in reconnect
       {
          If (FileExist(@[LP].dir) && reconnect.Remove(LP)){
             DllCall("CloseHandle","Uint",@[LP].hD)
             @[LP].hD:=DllCall("CreateFile","Str",StrLen(@[LP].dir)=3?SubStr(@[LP].dir,1,2):@[LP].dir,"UInt",0x1,"UInt",0x1|0x2|0x4
                   ,"UInt",0,"UInt",0x3,"UInt",0x2000000|0x40000000,"UInt",0)
             DllCall("ResetEvent","UInt",@[LP].O.hEvent)
             DllCall("ReadDirectoryChangesW","UInt",@[LP].hD,"UInt",@[LP].FNI[""],"UInt",sizeof_FNI
                ,"Int",@[LP].sD,"UInt",@[LP].CNG,"UInt",0,"UInt",@[LP].O[""],"UInt",0)
          }
       }
       if !( (r:=DllCall("MsgWaitForMultipleObjectsEx","UInt",#.MaxIndex()
                ,"UInt",DirEvents[""],"UInt",0,"UInt",0x4FF,"UInt",6))>=0
                && r<#.MaxIndex() ){
          return
       }
       DllCall("KillTimer", UInt,0, UInt,timer)
       LP:=#[r+1],DllCall("GetOverlappedResult","UInt",@[LP].hD,"UInt",@[LP].O[""],"UIntP",nReadLen,"Int",1)
       If (A_LastError=64){ ; ERROR_NETNAME_DELETED - The specified network name is no longer available.
          If !FileExist(@[LP].dir) ; If folder does not exist add to reconnect routine
             reconnect.Insert(LP,LP)
       } else
          Loop {
             FNI:=A_Index>1?(new _Struct(FILE_NOTIFY_INFORMATION,FNI[""]+FNI.NextEntryOffset)):(new _Struct(FILE_NOTIFY_INFORMATION,@[LP].FNI[""]))
             If (FNI.Action < 0x6){
                FileName:=@[LP].dir . StrGet(FNI.FileName[""],FNI.FileNameLength/2,"UTF-16")
                If ((FNI.Action=FILE_ACTION_RENAMED_OLD_NAME && FileFromOptional:=FileName)
                                 || @[LP].FLT="" || RegExMatch(FileName,@[LP].FLT) || RegExMatch(FileFrom,@[LP].FLT) || InStr(FileExist(FileName),"D"))
                   If (FNI.Action=FILE_ACTION_ADDED){
                      FileTo:=FileName
                   } else If (FNI.Action=FILE_ACTION_REMOVED){
                      FileFrom:=FileName
                   } else If (FNI.Action=FILE_ACTION_MODIFIED){
                      FileFrom:=FileTo:=FileName
                   } else If (FNI.Action=FILE_ACTION_RENAMED_OLD_NAME){
                      FileFrom:=FileName
                   } else If (FNI.Action=FILE_ACTION_RENAMED_NEW_NAME){
                      FileTo:=FileName
                   }
                                     If (FNI.Action != 4 && (FileTo . FileFrom) !="")
                                         @[LP].Func(FileFrom=""?FileFromOptional:FileFrom,FileTo)
                                         ,FileFrom:="",FileTo:="",FileFromOptional:=""
             }
          } Until (!FNI.NextEntryOffset || ((FNI[""]+FNI.NextEntryOffset) > (@[LP].FNI[""]+sizeof_FNI-12)))
       DllCall("ResetEvent","UInt",@[LP].O.hEvent)
       DllCall("ReadDirectoryChangesW","UInt",@[LP].hD,"UInt",@[LP].FNI[""],"UInt",sizeof_FNI
                ,"Int",@[LP].sD,"UInt",@[LP].CNG,"UInt",0,"UInt",@[LP].O[""],"UInt",0)
       timer:=DllCall("SetTimer","Uint",0,"UInt",timer,"Uint",50,"UInt",WatchDirectory)
       Return
    }
    Return
 }


/**
 * Helper Function
 *     Get the version ID of the current Windows installation
 *
 * @sample
 *     GetWindowsVersion()     ; ie: returns 10.0
 *
 * @return  integer
 */
GetWindowsVersion()
{
    Version := DllCall("GetVersion", "uint") & 0xFFFF
    return (Version & 0xFF) "." (Version >> 8)
}

/**
 * Helper Function
 *     Extract an icon from an executable, DLL or icon file.
 *
 * @sample
 *     ExtractIcon("C:\windows\system32\system.dll", 1)
 *
 * @param   string  Filename    Name of the ico, dll or exe from which to extract the icon
 * @param   integer IconNumber  Index of the icon in the file
 * @param   integer IconSize    Resolution of the icon
 * @return  bitmap
 */
ExtractIcon(Filename, IconNumber = 0, IconSize = 64)
{
    ; LoadImage is not used..
    ; ..with exe/dll files because:
    ;   it only works with modules loaded by the current process,
    ;   it needs the resource ordinal (which is not the same as an icon index), and
    ; ..with ico files because:
    ;   it can only load the first icon (of size %IconSize%) from an .ico file.

    ; If possible, use PrivateExtractIcons, which supports any size of icon.
    ; r:=DllCall("PrivateExtractIcons" , "str", Filename, "int", IconNumber-1, "int", IconSize, "int", IconSize, "Ptr*", h_icon, "PTR*", 0, "uint", 1, "uint", 0, "int")
    ; if !ErrorLevel
    ;    return h_icon
    r := DllCall("Shell32.dll\SHExtractIconsW", "str", Filename, "int", IconNumber-1, "int", IconSize, "int", IconSize, "Ptr*", h_icon, "Ptr*", pIconId, "uint", 1, "uint", 0, "int")
    If (!ErrorLevel && r != 0)
        return h_icon
    return 0
}

/**
  * Fake Debug function while a2 doesn't offer a global one
  */
WriteDebug(Title, InputObject = "", level = "info", module = "", delay = 0, Delimiter = "`n")
{
    _prefix := level ? "[" level "] " : ""
    _module := module ? "[" module "] " : ""
    _time   := "[" FormatTime(A_Now, "HH:mm:ss") "] "

    if (Settings.Debug.Enabled)
    {
        sleep, %delay%
        FileAppend % _time _prefix _module Title "`n", *
        if (InputObject)
        {
            Loop, Parse, InputObject, %Delimiter%
                WriteDebug("    " A_LoopField, "", level, module, delay)
        }
    }
}

/**
 * Helper Function
 *     Starts a timer that can cal functions and object methods
 *
 * @param   func    Function     A function or method reference to be called
 * @param   integer Period      Period/Timer in ms to call the Fcunction / value "OFF" deactivates a timer
 * @param           ParmObject
 * @param           Priority
 * @return
 */
SetTimerF( Function, Period=0, ParmObject=0, Priority=0 ) {
    Static current,tmrs:=Object() ;current will hold timer that is currently running
    If IsFunc( Function ) || IsObject( Function ) {
        if IsObject(tmr:=tmrs[Function]) ;destroy timer before creating a new one
            ret := DllCall( "KillTimer", UInt,0, UInt, tmr.tmr)
                , DllCall("GlobalFree", UInt, tmr.CBA)
                , tmrs.Remove(Function)
        if (Period = 0 || Period ? "off")
            return ret ;Return as we want to turn off timer
        ; create object that will hold information for timer, it will be passed trough A_EventInfo when Timer is launched
        tmr:=tmrs[Function]:=Object("func",Function,"Period",Period="on" ? 250 : Period,"Priority",Priority
                            ,"OneTime",(Period<0),"params",IsObject(ParmObject)?ParmObject:Object()
                            ,"Tick",A_TickCount)
        tmr.CBA := RegisterCallback(A_ThisFunc,"F",4,&tmr)
        return !!(tmr.tmr  := DllCall("SetTimer", UInt,0, UInt,0, UInt
                            , (Period && Period!="On") ? Abs(Period) : (Period := 250)
                            , UInt,tmr.CBA)) ;Create Timer and return true if a timer was created
                            , tmr.Tick:=A_TickCount
    }
    tmr := Object(A_EventInfo) ;A_Event holds object which contains timer information
    if IsObject(tmr) {
        DllCall("KillTimer", UInt,0, UInt,tmr.tmr) ;deactivate timer so it does not run again while we are processing the function
        If (!tmr.active && tmr.Priority<(current.priority ? current.priority : 0)) ;Timer with higher priority is already current so return
           Return (tmr.tmr:=DllCall("SetTimer", UInt,0, UInt,0, UInt, 100, UInt,tmr.CBA)) ;call timer again asap
        current:=tmr
        tmr.tick:=ErrorLevel :=Priority ;update tick to launch function on time
        func := tmr.func.(tmr.params*) ;call function
        current= ;reset timer
        if (tmr.OneTime) ;One time timer, deactivate and delete it
           return DllCall("GlobalFree", UInt,tmr.CBA)
                 ,tmrs.Remove(tmr.func)
        tmr.tmr:= DllCall("SetTimer", UInt,0, UInt,0, UInt ;reset timer
                ,((A_TickCount-tmr.Tick) > tmr.Period) ? 0 : (tmr.Period-(A_TickCount-tmr.Tick)), UInt,tmr.CBA)
    }
}

/**
 * Helper Function
 *     Returns the workspace area covered by the active monitor
 *
 * @param   var    MonLeft       Variable in which to write the monitor's left coords
 * @param   var    MonTop        Variable in which to write the monitor's top coords
 * @param   var    MonW          Variable in which to write the monitor's height
 * @param   var    MonH          Variable in which to write the monitor's height
 * @param   var    hWndOrMouseX  Window handler or Mouse X coords from which to guess the monitor in question
 * @param   var    MouseY                          Mouse Y coords from which to guess the monitor in question
 */
GetActiveMonitorWorkspaceArea(ByRef MonLeft, ByRef MonTop, ByRef MonW, ByRef MonH,hWndOrMouseX, MouseY = "")
{
    mon := GetActiveMonitor(hWndOrMouseX, MouseY)
    if (mon>=0)
    {
        SysGet, Mon, MonitorWorkArea, %mon%
        MonW := MonRight - MonLeft
        MonH := MonBottom - MonTop
    }
}

/**
 * Helper Function
 *     Returns the monitor the mouse or the active window is in
 *
 * @param   var    hWndOrMouseX  Window handler or Mouse X coords from which to guess the monitor in question
 * @param   var    MouseY                          Mouse Y coords from which to guess the monitor in question
 * @return  int   MonitorID
 */
GetActiveMonitor(hWndOrMouseX, MouseY = "")
{
    if (MouseY="")
    {
        WinGetPos,x,y,w,h,ahk_id %hWndOrMouseX%
        if (!x && !y && !w && !h)
        {
            MsgBox GetActiveMonitor(): invalid window handle!
            return -1
        }
        x := x + Round(w/2)
        y := y + Round(h/2)
    }
    else
    {
        x := hWndOrMouseX
        y := MouseY
    }
    ; Loop through every monitor and calculate the distance to each monitor
    iBestD := 0xFFFFFFFF
    SysGet, Mon0, MonitorCount
    Loop %Mon0% { ;Loop through each monitor
        SysGet, Mon%A_Index%, Monitor, %A_Index%
        Mon%A_Index%MidX := Mon%A_Index%Left + Ceil((Mon%A_Index%Right - Mon%A_Index%Left) / 2)
        Mon%A_Index%MidY := Mon%A_Index%Top + Ceil((Mon%A_Index%Top - Mon%A_Index%Bottom) / 2)
    }
    Loop % Mon0 {
      D := Sqrt((x - Mon%A_Index%MidX)**2 + (y - Mon%A_Index%MidY)**2)
      If (D < iBestD) {
         iBestD := D
         iMonitor := A_Index
      }
   }
   return iMonitor
}


TranslateMUI(resDll, resID)
{
    VarSetCapacity(buf, 256)
    hDll := DllCall("LoadLibrary", "str", resDll, "Ptr")
    Result := DllCall("LoadString", "Ptr", hDll, "uint", resID, "str", buf, "int", 128)
    return buf
}


/**
 * Helper Function
 *     Runs a command as user (whether as as admin)
 *
 * @param   string  Command     Command to be executed
 * @param   string  WorkingDir
 * @param   string  Options
 * @return  string  PID         ProcessID of the started command
 */
#include lib\ahklib\CNotification.ahk
RunAsUser(Command, WorkingDir = "", Options = "")
{
    result := DllCall(Settings.DllPath "\Explorer.dll\CreateProcessMediumIL", Str, Command, Str, WorkingDir, Str, Options, "UInt")
    if (A_LastError = 740) ;ERROR_ELEVATION_REQUIRED
    {
        Run, %Command% , %WorkingDir%, %Mode% UseErrorLevel, v
        if (A_LastError)
            Notify("Error", "Error launching " Target, 5, NotifyIcons.Error)
        Return, v
    }
}

/**
 * Helper Function
 *     Runs a command as admin
 *
 * @param   string  Command     Command to be executed
 * @param   string  WorkingDir
 * @param   string  Options
 * @return  bool                 Did user confirm the UAC dialog
 */
RunAsAdmin(Command, WorkingDir = "", Options = "")
{
    uacrep := DllCall("shell32\ShellExecute", uint, 0, str, "RunAs", str, Command, str, Options, str, WorkingDir, int, 1)
    return uacrep = 42 ;UAC dialog confirmed
}

; checks if a point is in a rectangle
IsInArea(px, py, x, y, w, h)
{
    return (px > x && py > y && px < x + w && py < y + h)
}

; Gets ClassNN from hwnd
HWNDToClassNN(hwnd)
{
    win := DllCall("GetParent", "PTR", hwnd, "PTR")
    WinGet ctrlList, ControlList, ahk_id %win%
    ; Built an array indexing the control names by their hwnd
    Loop Parse, ctrlList, `n
    {
        ControlGet hwnd1, Hwnd, , %A_LoopField%, ahk_id %win%
        if (hwnd1=hwnd)
        return A_LoopField
    }
}

; Gets width of all screens combined. NOTE: Single screens may have different vertical resolutions so some parts of the area returned here might not belong to any screens!
GetVirtualScreenCoordinates(ByRef x, ByRef y, ByRef w, ByRef h)
{
    SysGet, x, 76 ;Get virtual screen coordinates of all monitors
    SysGet, y, 77
    SysGet, w, 78
    SysGet, h, 79
}


fixMaximizedScreenCoord(Window, ByRef maxL, ByRef maxT, ByRef maxW, ByRef maxH, newBase=0)
{
    if ((Window == "A") OR (!Window))
        Monitor := GetMonitorIndexFromWindow(WinExist("A"))
    else {
        WinGetPos, WinX, WinY, WinW, WinH, % Window
        Monitor := GetMonitorIndexFromCoords(WinX ", " WinY ", " WinW ", " WinH)
    }
    Monitor := Monitor ? Monitor : 0

    SysGet, tempArea, MonitorWorkArea, % Monitor
    SysGet, WorkArea, MonitorWorkArea, % Monitor
    SysGet, Monitor, Monitor, % Monitor
    WorkAreaWidth := WorkAreaRight - WorkAreaLeft
    WorkAreaHeight := WorkAreaBottom - WorkAreaTop
    MonitorWidth := MonitorRight - MonitorLeft
    MonitorHeight := MonitorBottom - MonitorTop

    If (tempAreaLeft < WorkAreaLeft)
        WorkAreaLeft := tempAreaLeft
    If (tempAreaRight > WorkAreaRight)
        WorkAreaRight := tempAreaRight
    If (tempAreaTop < WorkAreaTop)
        WorkAreaTop := tempAreaTop
    If (tempAreaBottom > WorkAreaBottom)
        WorkAreaBottom := tempAreaBottom

    WinGet, MinMax, MinMax, "ahk_id " hWnd
    WinGet, Style, Style, "ahk_id " hWnd
    If (MinMax = 1 AND (Style & 0x40000)) {
        If (maxL < WorkArea%scr_Monitor%Left)
            maxL := ( (newBase=1) ? (maxW-WorkAreaWidth)/2 : WorkAreaLeft)
        If (maxT < WorkAreaTop)
            maxT := ( (newBase=1) ? (maxH-WorkAreaHeight)/2 : WorkAreaTop)
        If (maxW > WorkAreaWidth)
            maxW := ( (newBase=1) ? WorkAreaWidth : WorkAreaWidth)
        If (maxH > WorkAreaHeight)
            maxH := ( (newBase=1) ? WorkAreaHeight : WorkAreaHeight)
    }
    Else If newBase = 1
    {
        maxL = 0
        maxT = 0
    }
}


extract_integer(ByRef pSource, pOffset=0, pIsSigned=false, pSize=4)
{
	; pSource is a string (buffer) whose memory area contains a raw/binary integer at pOffset.
	; The caller should pass true for pSigned to interpret the result as signed vs. unsigned.
	; pSize is the size of PSource's integer in bytes (e.g. 4 bytes for a DWORD or Int).
	; pSource must be ByRef to avoid corruption during the formal-to-actual copying process
	; (since pSource might contain valid data beyond its first binary zero).
	Loop %pSize%  ; Build the integer by adding up its bytes.
		result += *(&pSource + pOffset + A_Index-1) << 8*(A_Index-1)
	if (!pIsSigned OR pSize > 4 OR result < 0x80000000)
		return result  ; Signed vs. unsigned doesn't matter in these cases.
	; Otherwise, convert the value (now known to be 32-bit) to its signed counterpart:
	return -(0xFFFFFFFF - result + 1)
}
