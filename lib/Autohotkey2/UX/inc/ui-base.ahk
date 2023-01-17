class AutoHotkeyUxGui extends Gui {
    __new(title, opt:='') {
        super.__new(opt, title, this)
        this.SetFont('s9', "Segoe UI")
        this.OnEvent('Escape', 'Destroy')
        this.OnEvent('Close', 'Destroy')
    }
    
    AddListMenu(options:='', columns:=unset) {
        IsSet(columns) || columns := []
        c := this.AddListView(UxListMenu.DefaultOptions ' ' options, columns)
        if !InStr(options, 'Theme')
            DllCall("uxtheme\SetWindowTheme", "ptr", c.hwnd, "wstr", "Explorer", "ptr", 0)
        static LVTVIM_TILESIZE := 1, LVTVIM_COLUMNS := 2, LVTVIM_LABELMARGIN := 4
        static LVTVIF_AUTOSIZE := 0, LVTVIF_EXTENDED := 4, LVTVIF_FIXEDHEIGHT := 2
            , LVTVIF_FIXEDSIZE := 3, LVTVIF_FIXEDWIDTH := 1
        static LVM_SETTILEVIEWINFO := 0x10A2
        tileviewinfo := Buffer(40, 0)
        ControlGetPos(,, &w,, c)
        pad := 2 * A_ScreenDPI // 96
        NumPut(
            'uint', 40, ; cbSize
            'uint', LVTVIM_LABELMARGIN | LVTVIM_TILESIZE, ; dwMask
            'uint', LVTVIF_FIXEDWIDTH, ; dwFlags
            'int', w, 'int', 0, ; sizeTile
            'int', 0, ; cLines
            'int', pad, 'int', pad, 'int', pad, 'int', pad, ; rcLabelMargin
            tileviewinfo
        )
        SendMessage LVM_SETTILEVIEWINFO,, tileviewinfo, c
        c.base := UxListMenu.Prototype
        return c
    }
    
    AddIconButton(options, iconHandle, hiddenText:="") {
        static BS_ICON := 0x40
        static BS_CENTER := 0x300
        static BS_VCENTER := 0xC00
        btn := this.AddButton((BS_ICON | BS_CENTER | BS_VCENTER) ' ' options, hiddenText)
        static BM_SETIMAGE := 0xF7
        SendMessage(BM_SETIMAGE, 1, iconHandle, btn)
        return btn
    }
    
    FileSelect(p*) {
        this.Opt '+OwnDialogs'
        try
            return FileSelect(p*)
        finally
            this.Opt '-OwnDialogs'
    }
    
    static Show(p*) {
        for w in WinGetList('ahk_pid ' ProcessExist())
            if (g := GuiFromHwnd(w)) && g.base = this.Prototype
                return g.Show()
        inst := this(p*)
        inst.Show()
    }
}

class UxListMenu extends Gui.ListView {
    static DefaultOptions := '-Multi Tile'
        . ' R1'
        . ' -E0x200' ; -WS_EX_CLIENTEDGE (remove border)
        . ' LV0x14000'
        . Format(' Background{:x}', DllCall("GetSysColor", "int", 15, "int")) ; COLOR_3DFACE
    
    Add(p*) {
        i := super.Add(p*)
        static LVM_SETTILEINFO := 0x10A4
        static LVCFMT_FILL := 0x200000
        static LVCFMT_WRAP := 0x400000
        tileinfo := Buffer(8 + 3*A_PtrSize, 0)
        col := Buffer(4)
        colf := Buffer(4)
        NumPut("int", 1, col)
        NumPut("int", LVCFMT_FILL | LVCFMT_WRAP, colf)
        NumPut("int", tileinfo.size, "int", i-1, "uptr", 1, "ptr", col.ptr, "ptr", colf.ptr, tileinfo)
        SendMessage(LVM_SETTILEINFO, 0, tileinfo, this)
        return i
    }
    
    _SetTileWidth(w) {
        static LVTVIM_TILESIZE := 1, LVTVIM_COLUMNS := 2, LVTVIM_LABELMARGIN := 4
        static LVTVIF_AUTOSIZE := 0, LVTVIF_EXTENDED := 4, LVTVIF_FIXEDHEIGHT := 2
            , LVTVIF_FIXEDSIZE := 3, LVTVIF_FIXEDWIDTH := 1
        static LVM_SETTILEVIEWINFO := 0x10A2
        tileviewinfo := Buffer(40, 0)
        pad := 2 * A_ScreenDPI // 96
        NumPut(
            'uint', 40, ; cbSize
            'uint', LVTVIM_LABELMARGIN | LVTVIM_TILESIZE, ; dwMask
            'uint', LVTVIF_FIXEDWIDTH, ; dwFlags
            'int', w, 'int', 0, ; sizeTile
            'int', 0, ; cLines
            'int', pad, 'int', pad, 'int', pad, 'int', pad, ; rcLabelMargin
            tileviewinfo
        )
        SendMessage LVM_SETTILEVIEWINFO,, tileviewinfo, this
    }
    
    AutoSize(maxItems:=20) {
        static LVM_GETITEMRECT := 0x100E, LVIR_BOUNDS := 0
        static SM_CXVSCROLL := 2
        
        itemCount := this.GetCount()
        
        ; Keep control width and adjust tile width to avoid horizontal scrollbar.
        ControlGetPos(,, &w,, this)
        if itemCount > maxItems
            w -= SysGet(SM_CXVSCROLL)
        this._SetTileWidth(w)
        
        ; Adjust control height to fit content.
        rect := Buffer(16, 0)
        NumPut('int', LVIR_BOUNDS, rect)
        SendMessage(LVM_GETITEMRECT, Min(itemCount, maxItems) - 1, rect.ptr, this)
        iy := NumGet(rect, 4, 'int')
        iw := NumGet(rect, 8, 'int')
        ih := NumGet(rect, 12, 'int') - iy
        ; Result needs additional padding.  Testing showed the width returned was less
        ; than what we set with LVM_SETTILEVIEWINFO.  The amount of padding needed to
        ; avoid scrollbars appeared to be exactly the amount to bring it up to the size
        ; we specified, so perhaps something similar is happening with the height.
        h := NumGet(rect, 12, 'int') + 4
        ControlMove(,,, h, this)
    }
}