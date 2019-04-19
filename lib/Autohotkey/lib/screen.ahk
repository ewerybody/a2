; Gets width of all screens combined. NOTE: Single screens may have different vertical resolutions so some parts of the area returned here might not belong to any screens!
screen_get_virtual_size(ByRef x, ByRef y, ByRef w, ByRef h)
{
    SysGet, x, 76 ;Get virtual screen coordinates of all monitors
    SysGet, y, 77
    SysGet, w, 78
    SysGet, h, 79
}


 /**
 * Helper Function
 *     Returns the MonitorID where the specified window is located on
 *     By shnywong
 *
 * @sample
 *     screen_get_index(WinExist("A"))
 *
 * @param   HWND     hwnd     Handler of the window to be found
 * @return  integer
 *
 * @docu    https://autohotkey.com/board/topic/69464-how-to-determine-a-window-is-in-which-monitor/#entry440355
 */
screen_get_index(hwnd)
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
