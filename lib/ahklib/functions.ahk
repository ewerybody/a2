
getSelection( clipWaitTime=0.5 )
{
    SavedClipboard := ClipboardAll
    Clipboard =
    Sleep, 0

    ; also watch for the process-executable instead of just window title:
    WinGetClass, Class, A
    WinGet, this_process, ProcessName, ahk_class %Class%

    ; sending keystroke Ctrl+C in maya can cause a "scene clipboard save" which can be heavy
    ; to avoid this we go sure we are in the text editor window of maya
    if (this_process == "maya.exe")
    {
        WinGetTitle, this_title, A
        if (this_title != "Script Editor")
            Return ""
    }

    ;Send, {Blind}%resetModifiers%^c%restoreModifiers%
    if (this_process == "Photoshop.exe")
    {
        SetKeyDelay, 20, 20
        SendEvent, {Ctrl down}^c{Ctrl up}
    }
    Else If Class in PuTTY,ConsoleWindowClass,ytWindow
        Send, {ENTER}
    Else
        Send, {Ctrl down}^c{Ctrl up}

    If clipWaitTime <>
    {
        If copyAsText = 0
            ClipWait, %clipWaitTime%, 1
        Else
            ClipWait, %clipWaitTime%
    }
    Sleep,0

    Selection := Clipboard
    Clipboard := SavedClipboard

    Return Selection
}


; good ol getSelection function from ac'tivAid
; copyOnly=1 to actually fill the clipboard
aagetSelection( copyAsText=1, copyOnly=0, clipWaitTime=0.5 )
{
    global Selection, SavedClipboard, NoOnClipboardChange
    NoOnClipboardChange = 1

    ; also watch for the process-executable instead of just window title:
    WinGetClass, Class, A
    WinGet, this_process, ProcessName, ahk_class %Class%

    ; sending keystroke Ctrl+C in maya can cause a "scene clipboard save" which can be heavy
    ; to avoid this we go sure we are in the text editor window of maya
    if (this_process == "maya.exe")
    {
        WinGetTitle, this_title, A
        if (this_title != "Script Editor")
        {
            Selection := ""
            Return
        }
    }

    ;Send, {Blind}%resetModifiers%^c%restoreModifiers%
    if (this_process == "Photoshop.exe")
    {
        SetKeyDelay, 20, 20
        SendEvent, {Ctrl down}^c{Ctrl up}
    }
    Else If Class in PuTTY,ConsoleWindowClass,ytWindow
        Send, {ENTER}
    Else
        Send, {Ctrl down}^c{Ctrl up}

    if (this_process == "Photoshop.exe")
    {
        Gui, 99:+ToolWindow
        Gui, 99:Show, x-1000 y-1000 w10 h10
    }

    If clipWaitTime <>
    {
        If copyAsText = 0
            ClipWait, %clipWaitTime%, 1
        Else
            ClipWait, %clipWaitTime%
    }
    Sleep,0

    if (this_process == "Photoshop.exe")
    {
        Sleep,10
        Gui, 99:Destroy
    }

    If copyAsText = 1
        Selection := Clipboard
    ;Else If copyAsText in Unicode,UTF8,UTF-8
    ;{
    ;   Transform, Selection, Unicode
    ;   ;msgbox, % Ansi2UTF8(UTF82Ansi(Selection)) "`n" Selection
    ;   If (Ansi2UTF8(UTF82Ansi(Selection)) = Selection)
    ;       Selection := Clipboard
    ;}
    Else
        Selection := ClipboardAll

    If copyOnly = 0
    {
        Sleep, 20
        Clipboard := SavedClipboard
    }
    Sleep,0

    NoOnClipboardChange =

    If copyAsText = 1
        Return Selection
}

; to remove whitespace from strings start + end
trim(string)
{
    start := 1
    stringLen, end, string
    loop, %end% ; fix the start
    {
        l := SubStr(string, A_Index, 1)
        if (l != A_Space && l != A_Tab && l != "`n" && l != "`r")
        {
            start := A_Index
            break
        }
    }
    string := SubStr(string, start)
    stringLen, end, string
    loop, %end% ; fix the end
    {
        i := - A_Index + 1
        l := SubStr(string, i, 1)
        if (l != A_Space && l != A_Tab && l != "`n" && l != "`r")
        {
            end := A_Index - 1
            break
        }
    }
    StringTrimRight, string, string, %end%
    return string
}


; WIP: Which version do you like more?!?!
; strips whitespace from start and end of a string:
strip(byref inputString)
{
    ; if first char is space, tab or linefeed, remove it and look again:
    c := SubStr(inputString, 1, 1)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimLeft, inputString, inputString, 1
        strip(inputString)
    }
    ; now last character:
    c := SubStr(inputString, 0)
    if (c == A_Space OR c == A_Tab OR c == "`n" OR c == "`r")
    {
        StringTrimRight, inputString, inputString, 1
        strip(inputString)
    }
}

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

; checks for some aspects to assume that the given string is a URL
; TODO: this can probably be done much much better!!!...
isURL(byref str)
{
    ; look if the start of the string is url like
    if (SubStr(str,1,7) == "http://" || SubStr(str,1,8) == "https://" || SubStr(str,1,4) == "www.")
        return true
    ; now the end of the string
    if (SubStr(str,-3,4) == ".htm" || SubStr(str,-4,5) == ".html")
        return true
    ; now if inbetween are TLDs like .com, .de, .co.uk ...
    else
    {
        dotpos := InStr(str,".")
        sub := SubStr(str,dotpos,3)
        if (sub == ".de" || sub == ".at" || sub == ".ch")
            return true
        sub := SubStr(str,dotpos,4)
        if (sub == ".com" || sub == ".org" || sub == ".net")
            return true
        if (SubStr(str,dotpos,6) == ".co.uk")
            return true
    }
    return false
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
 *     Expand path placeholders
 *     It's basically ExpandEnvironmentStrings() with some additional directories
 *
 * @sample
 *     ExpandPathPlaceholders("%ProgramFiles")
 * @sample
 *     ExpandPathPlaceholders("Temp")
 *
 * @param   string  InputString     The path to be resolved
 * @return  string
 *
 * @docu   https://msdn.microsoft.com/en-us/library/windows/desktop/ms724265(v=vs.85).aspx
 */
ExpandPathPlaceholders(InputString)
{
    static Replacements := {  "Desktop" :             GetFullPathName(A_Desktop)
                            , "MyDocuments" :        GetFullPathName(A_MyDocuments)
                            , "StartMenu" :            GetFullPathName(A_StartMenu)
                            , "StartMenuCommon" :     GetFullPathName(A_StartMenuCommon)
                            , "a2Dir" :            A_ScriptDir "\.."}
    if (!Replacements.7plusDrive)
    {
        SplitPath, A_ScriptDir,,,,,s7plusDrive
        Replacements.7plusDrive := s7plusDrive
    }
    Replacements.ImageEditor := Settings.Misc.DefaultImageEditor
    Replacements.TextEditor := Settings.Misc.DefaultTextEditor

    for Placeholder, Replacement in Replacements
        while(InStr(InputString, Placeholder) && A_Index < 10)
            StringReplace, InputString, InputString, % "%" Placeholder "%", % Replacement, All

    ; get the required size for the expanded string
    SizeNeeded := DllCall("ExpandEnvironmentStrings", "Str", InputString, "PTR", 0, "Int", 0)
    if (SizeNeeded == "" || SizeNeeded <= 0)
        return InputString ; unable to get the size for the expanded string for some reason

    ByteSize := SizeNeeded * 2 + 2
    VarSetCapacity(TempValue, ByteSize, 0)

    ; attempt to expand the environment string
    if (!DllCall("ExpandEnvironmentStrings", "Str", InputString, "Str", TempValue, "Int", SizeNeeded))
        return InputString ; unable to expand the environment string
    return TempValue
}

/**
 * Helper Function
 *     Converts the specified path to its long form.
 *
 * @sample
 *     GetFullPathName("C:\Progr~1")  -> "C:\Program Files"
 *
 * @param   string  sPath       The path to be converted.
 * @return  string
 *
 * @docu    https://msdn.microsoft.com/en-us/library/windows/desktop/aa364980(v=vs.85).aspx
 */
GetFullPathName(sPath)
{
    VarSetCapacity(lPath,A_IsUnicode ? 520 : 260, 0)
    DllCall("GetLongPathName", Str, sPath, Str, lPath, UInt, 260)
    return lPath
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
