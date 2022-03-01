MouseOverCondition(MouseOverType) {
    /* if(MouseOverType = "Window") {
        MouseGetPos,,,window
        return WindowFilterMatches(window)
    }
    else
    */
    if (MouseOverType = "Clock")
        return IsMouseOverClock()
    else if (MouseOverType = "Tray")
        return IsMouseOverTray()
    else {
        result := MouseHitTest()
        if(MouseOverType = "TitleBar")
            return result = 2
        else if(MouseOverType = "MinimizeButton")
            return result = 8
        else if(MouseOverType = "MaximizeButton")
            return result = 9
        else if(MouseOverType = "CloseButton")
            return result = 20
    }
}

IsMouseOverClock() {
    CoordMode, Mouse, Screen
    MouseGetPos, , , , ControlUnderMouse
    return (ControlUnderMouse = "TrayClockWClass1") ? true : false
}

IsMouseOverTray() {
    MouseGetPos,,,TargetWindow
    class := WinGetClass("ahk_id " TargetWindow)
    return (class == "Shell_TrayWnd") ? true : false
}

/*
Performs a hittest on the window under the mouse and returns the WM_NCHITTEST Result
#define HTERROR             (-2)
#define HTTRANSPARENT       (-1)
#define HTNOWHERE           0
#define HTCLIENT            1
#define HTCAPTION           2
#define HTSYSMENU           3
#define HTGROWBOX           4
#define HTSIZE              HTGROWBOX
#define HTMENU              5
#define HTHSCROLL           6
#define HTVSCROLL           7
#define HTMINBUTTON         8
#define HTMAXBUTTON         9
#define HTLEFT              10
#define HTRIGHT             11
#define HTTOP               12
#define HTTOPLEFT           13
#define HTTOPRIGHT          14
#define HTBOTTOM            15
#define HTBOTTOMLEFT        16
#define HTBOTTOMRIGHT       17
#define HTBORDER            18
#define HTREDUCE            HTMINBUTTON
#define HTZOOM              HTMAXBUTTON
#define HTSIZEFIRST         HTLEFT
#define HTSIZELAST          HTBOTTOMRIGHT
#if(WINVER >= 0x0400)
#define HTOBJECT            19
#define HTCLOSE             20
#define HTHELP              21
*/
MouseHitTest() {
    CoordMode, Mouse, Screen
    MouseGetPos, MouseX, MouseY, WindowUnderMouseID
    WinGetClass, winclass , ahk_id %WindowUnderMouseID%
    if winclass in BaseBar,D2VControlHost,Shell_TrayWnd,WorkerW,ProgMan  ; make sure we're not doing this on the taskbar
        return -2
    ; WM_NCHITTEST
    SendMessage, 0x84,, ( (MouseY&0xFFFF) << 16 )|(MouseX&0xFFFF),, ahk_id %WindowUnderMouseID%
    return ErrorLevel
}

