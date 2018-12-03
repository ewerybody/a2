; Gets width of all screens combined. NOTE: Single screens may have different vertical resolutions so some parts of the area returned here might not belong to any screens!
screen_get_virtual_size(ByRef x, ByRef y, ByRef w, ByRef h)
{
    SysGet, x, 76 ;Get virtual screen coordinates of all monitors
    SysGet, y, 77
    SysGet, w, 78
    SysGet, h, 79
}
