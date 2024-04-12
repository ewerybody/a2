screen_get_virtual_size(&x, &y, &w, &h) {
    ; Get width of all screens combined.
    ; NOTE: Single screens may have different vertical resolutions so some parts of
    ; the area returned here might not belong to any screens!
    x := SysGet(76)
    y := SysGet(77)
    w := SysGet(78)
    h := SysGet(79)
}

screen_get_index(hwnd) {
    ; Return the MonitorID where the specified window is located on
    ; @author shnywong
    ; @docu
    ;     https://autohotkey.com/board/topic/69464-how-to-determine-a-window-is-in-which-monitor/#entry440355
    ; @sample
    ;     screen_get_index(WinExist("A"))
    ; @param   HWND     hwnd     Handler of the window to be found
    ; @return  integer
    ; Starts with 1.
    monitorIndex := 1

    monitorHandle := DllCall("MonitorFromWindow", "uint", hwnd, "uint", 0x2)
    if !monitorHandle
        return monitorIndex

    monitorInfo := Buffer(40)
    NumPut("uint", 40, monitorInfo)

    DllCall("GetMonitorInfo", "uint", monitorHandle, "ptr", monitorInfo)

    monitorLeft := NumGet(monitorInfo, 4, "Int")
    monitorTop := NumGet(monitorInfo, 8, "Int")
    monitorRight := NumGet(monitorInfo, 12, "Int")
    monitorBottom := NumGet(monitorInfo, 16, "Int")

    Loop(MonitorGetCount())
    {
        ; tempMon := SysGet , Monitor, %%
        MonitorGet(A_Index, &Left, &Top, &Right, &Bottom)

        ; Compare location to determine the monitor index.
        if ((monitorLeft = Left) and (monitorTop = Top)
            and (monitorRight = Right) and (monitorBottom = Bottom))
        {
            monitorIndex := A_Index
            break
        }
    }

    return monitorIndex
}

class Screen_Workarea {
    __new(index:=1) {
        ; SysGet WorkArea, MonitorWorkArea, %index%
        MonitorGetWorkArea(index, &Left, &Top, &Right, &Bottom)
        this.left := Left
        this.x := this.left
        this.right := Right
        this.x2 := this.right

        this.top := Top
        this.y := this.top
        this.bottom	:= Bottom
        this.y2 := this.bottom

        this.width := Right - Left
        this.w := this.width
        this.height := Bottom - Top
        this.h := this.height
    }
}

screen_get_work_area(monitor_index := -1) {
    ; Get a Screen_Workarea object of the currently active (where the active window is)
    ; or from the monitor with the given number.
    if (monitor_index == -1) {
        monitor_index := screen_get_index(WinExist("A"))
    }
    area := Screen_WorkArea(monitor_index)
    return area
}
