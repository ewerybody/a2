; GDIplus library cooked down from the Gdip standard library
; originally from tiq, maintained by Marius Sucan:
; https://github.com/marius-sucan/AHK-GDIp-Library-Compilation
; Thank you all!

gdipbitmap_from_area(x, y, w, h, Raster:="") {
    hhdc := 0
    Static Ptr := "UPtr"

    chdc := CreateCompatibleDC()
    hbm := CreateDIBSection(w, h, chdc)
    obm := SelectObject(chdc, hbm)
    hhdc := GetDC()

    BitBlt(chdc, 0, 0, w, h, hhdc, x, y, Raster)
    ReleaseDC(hhdc)

    pBitmap := gdipbitmap_CreateFromHBITMAP(hbm)
    SelectObject(chdc, obm)
    DeleteObject(hbm)
    DeleteDC(hhdc)
    DeleteDC(chdc)
    return pBitmap
}


gdipbitmap_from_screens(Raster:="") {
    ; Get a bitmap from all available screens.
    ; may contain blank areas when screens have different sizes.
    screen_get_virtual_size(x, y, w, h)
    return gdipbitmap_from_area(x, y, w, h, Raster)
}


gdipbitmap_from_screen(screen_number, Raster:="") {
    ; Get a bitmap from a given monitor or screen number.
    M := GetMonitorInfo(screen_number)
    x := M.Left, y := M.Top
    w := M.Right-M.Left, h := M.Bottom-M.Top
    return gdipbitmap_from_area(x, y, w, h, Raster)
}


gdipbitmap_from_handle(hwnd) {
    ; Get the area of a given handle, make sure its visible and
    ; shoot a bitmap from that area.
    window_activate(hwnd)
    geometry := window_get_geometry(hwnd)
    return gdipbitmap_from_area(geometry.x, geometry.y, geometry.w, geometry.h)
}


gdipbitmap_CreateFromHBITMAP(hBitmap, Palette:=0) {
    Ptr := A_PtrSize ? "UPtr" : "UInt"
    pBitmap := 0
    DllCall("gdiplus\GdipCreateBitmapFromHBITMAP"
        , Ptr, hBitmap
        , Ptr, Palette
        , A_PtrSize ? "UPtr*" : "uint*"
        , pBitmap)
    return pBitmap
}


gdipbitmap_to_file(pBitmap, sOutput, Quality:=75) {
    ; Save a bitmap to a file in any supported format onto disk.
    ;
    ; pBitmap   Pointer to a bitmap
    ; sOutput   Name of the file that the bitmap will be saved to. Supported extensions are:
    ;           .BMP,.DIB,.RLE,.JPG,.JPEG,.JPE,.JFIF,.GIF,.TIF,.TIFF,.PNG.
    ; Quality   If saving as jpg (.JPG,.JPEG,.JPE,.JFIF) then quality can be
    ;           1-100 with default at maximum quality.
    ;
    ; return    If the function succeeds, the return value is zero, otherwise:
    ;		    -1 = Extension supplied is not a supported file format
    ;		    -2 = Could not get a list of encoders on system
    ;		    -3 = Could not find matching encoder for specified file format
    ;		    -4 = Could not get WideChar name of output file
    ;		    -5 = Could not save file to disk
    ;
    ; notes	    This function will use the extension supplied from the sOutput
    ;           parameter to determine the output format.
	Ptr := A_PtrSize ? "UPtr" : "UInt"
	nCount := 0
	nSize := 0
	_p := 0

	SplitPath sOutput,,, Extension
	if !RegExMatch(Extension, "^(?i:BMP|DIB|RLE|JPG|JPEG|JPE|JFIF|GIF|TIF|TIFF|PNG)$")
		return -1
	Extension := "." Extension

	DllCall("gdiplus\GdipGetImageEncodersSize", "uint*", nCount, "uint*", nSize)
	VarSetCapacity(ci, nSize)
	DllCall("gdiplus\GdipGetImageEncoders", "uint", nCount, "uint", nSize, Ptr, &ci)
	if !(nCount && nSize)
		return -2

	If (A_IsUnicode){
		StrGet_Name := "StrGet"

		N := (A_AhkVersion < 2) ? nCount : "nCount"
		Loop %N%
		{
			sString := %StrGet_Name%(NumGet(ci, (idx := (48+7*A_PtrSize)*(A_Index-1))+32+3*A_PtrSize), "UTF-16")
			if !InStr(sString, "*" Extension)
				continue

			pCodec := &ci+idx
			break
		}
	} else {
		N := (A_AhkVersion < 2) ? nCount : "nCount"
		Loop %N%
		{
			Location := NumGet(ci, 76*(A_Index-1)+44)
			nSize := DllCall("WideCharToMultiByte", "uint", 0, "uint", 0, "uint", Location, "int", -1, "uint", 0, "int",  0, "uint", 0, "uint", 0)
			VarSetCapacity(sString, nSize)
			DllCall("WideCharToMultiByte", "uint", 0, "uint", 0, "uint", Location, "int", -1, "str", sString, "int", nSize, "uint", 0, "uint", 0)
			if !InStr(sString, "*" Extension)
				continue

			pCodec := &ci+76*(A_Index-1)
			break
		}
	}

	if !pCodec
		return -3

	if (Quality != 75)
	{
		Quality := (Quality < 0) ? 0 : (Quality > 100) ? 100 : Quality
		if RegExMatch(Extension, "^\.(?i:JPG|JPEG|JPE|JFIF)$")
		{
			DllCall("gdiplus\GdipGetEncoderParameterListSize", Ptr, pBitmap, Ptr, pCodec, "uint*", nSize)
			VarSetCapacity(EncoderParameters, nSize, 0)
			DllCall("gdiplus\GdipGetEncoderParameterList", Ptr, pBitmap, Ptr, pCodec, "uint", nSize, Ptr, &EncoderParameters)
			nCount := NumGet(EncoderParameters, "UInt")
			N := (A_AhkVersion < 2) ? nCount : "nCount"
			Loop %N%
			{
				elem := (24+(A_PtrSize ? A_PtrSize : 4))*(A_Index-1) + 4 + (pad := A_PtrSize = 8 ? 4 : 0)
				if (NumGet(EncoderParameters, elem+16, "UInt") = 1) && (NumGet(EncoderParameters, elem+20, "UInt") = 6)
				{
					_p := elem+&EncoderParameters-pad-4
					NumPut(Quality, NumGet(NumPut(4, NumPut(1, _p+0)+20, "UInt")), "UInt")
					break
				}
			}
		}
	}

	if (!A_IsUnicode)
	{
		nSize := DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sOutput, "int", -1, Ptr, 0, "int", 0)
		VarSetCapacity(wOutput, nSize*2)
		DllCall("MultiByteToWideChar", "uint", 0, "uint", 0, Ptr, &sOutput, "int", -1, Ptr, &wOutput, "int", nSize)
		VarSetCapacity(wOutput, -1)
		if !VarSetCapacity(wOutput)
			return -4
		_E := DllCall("gdiplus\GdipSaveImageToFile", Ptr, pBitmap, Ptr, &wOutput, Ptr, pCodec, "uint", _p ? _p : 0)
	}
	else
		_E := DllCall("gdiplus\GdipSaveImageToFile", Ptr, pBitmap, Ptr, &sOutput, Ptr, pCodec, "uint", _p ? _p : 0)
	return _E ? -5 : 0
}


CreateCompatibleDC(hdc:=0) {
    ; Create a memory device context (DC) compatible with the specified device.
    ;
    ; If this handle is 0 (by default), the function creates a memory device context
    ; compatible with the application's current screen.
    ; hdc		Handle to an existing device context.
    ; return	Handle to a device context or 0 on failure.
    return DllCall("CreateCompatibleDC", A_PtrSize ? "UPtr" : "UInt", hdc)
}


SelectObject(hdc, hgdiobj) {
    ; Select object into the specified device context (DC).
    ; The new object replaces the previous object of the same type.
    ;
    ; hdc       Handle to a DC
    ; hgdiobj   A handle to the object to be selected into the DC
    ;
    ; return    If the selected object is not a region and the function succeeds,
    ;           the return value is a handle to the object being replaced.
    ;
    ; notes     The specified object must have been created by using one of the following functions
    ;           Bitmap - CreateBitmap, CreateBitmapIndirect, CreateCompatibleBitmap, CreateDIBitmap,
    ;           CreateDIBSection (A single bitmap cannot be selected into more than one DC at the
    ;           same time)
    ;           Brush - CreateBrushIndirect, CreateDIBPatternBrush, CreateDIBPatternBrushPt,
    ;           CreateHatchBrush, CreatePatternBrush, CreateSolidBrush
    ;           Font - CreateFont, CreateFontIndirect
    ;           Pen - CreatePen, CreatePenIndirect
    ;           Region - CombineRgn, CreateEllipticRgn, CreateEllipticRgnIndirect, CreatePolygonRgn,
    ;           CreateRectRgn, CreateRectRgnIndirect
    ;
    ; notes     If the selected object is a region and the function succeeds,
    ;           the return value is one of the following value.
    ;
    ; NULLREGION    = 1 Region is empty
    ; SIMPLEREGION  = 2 Region consists of a single rectangle
    ; COMPLEXREGION = 3 Region consists of more than one rectangle
    Ptr := A_PtrSize ? "UPtr" : "UInt"
    return DllCall("SelectObject", Ptr, hdc, Ptr, hgdiobj)
}


DeleteObject(hObject) {
    ; Delete logical pen, brush, font, bitmap, region, or palette, freeing all system resources
    ; associated with the object.
    ; After the object is deleted, the specified handle is no longer valid.
    ;
    ; hObject   Handle to a logical pen, brush, font, bitmap, region, or palette to delete.
    ;
    ; return    Nonzero indicates success. Zero indicates that the specified handle is not valid
    ; or that the handle is currently selected into a device context.
    return DllCall("DeleteObject", A_PtrSize ? "UPtr" : "UInt", hObject)
}


GetDC(hwnd:=0) {
    ; Retrieve handle to a display device context (DC) for the client area of the specified window.
    ; The display device context can be used in subsequent graphics display interface (GDI)
    ; functions to draw in the client area of the window.
    ;
    ; hwnd	  Handle to the window whose device context is to be retrieved. If this value is NULL,
    ;         GetDC retrieves the device context for the entire screen.
    ;
    ; return  The handle the device context for the specified window's client area indicates
    ;         success. NULL indicates failure.
    return DllCall("GetDC", A_PtrSize ? "UPtr" : "UInt", hwnd)
}


GetDCEx(hwnd, flags:=0, hrgnClip:=0) {
    ; DCX_CACHE = 0x2
    ; DCX_CLIPCHILDREN = 0x8
    ; DCX_CLIPSIBLINGS = 0x10
    ; DCX_EXCLUDERGN = 0x40
    ; DCX_EXCLUDEUPDATE = 0x100
    ; DCX_INTERSECTRGN = 0x80
    ; DCX_INTERSECTUPDATE = 0x200
    ; DCX_LOCKWINDOWUPDATE = 0x400
    ; DCX_NORECOMPUTE = 0x100000
    ; DCX_NORESETATTRS = 0x4
    ; DCX_PARENTCLIP = 0x20
    ; DCX_VALIDATE = 0x200000
    ; DCX_WINDOW = 0x1
    Ptr := A_PtrSize ? "UPtr" : "UInt"
    return DllCall("GetDCEx", Ptr, hwnd, Ptr, hrgnClip, "int", flags)
}


ReleaseDC(hdc, hwnd:=0) {
    ; Release device context (DC), freeing it for use by other applications.
    ;
    ; The effect of ReleaseDC depends on the type of device context.
    ; The application must call the ReleaseDC function for each call to the
    ; GetWindowDC function and for each call to the GetDC function that
    ; retrieves a common device context. An application cannot use the ReleaseDC
    ; function to release a device context that was created by calling the
    ; CreateDC function; instead, it must use the DeleteDC function.
    ;
    ; hdc		Handle to the device context to be released.
    ; hwnd		Handle to the window whose device context is to be released.
    ;
    ; return	1 = released
    ;			0 = not released
    Ptr := A_PtrSize ? "UPtr" : "UInt"
    return DllCall("ReleaseDC", Ptr, hwnd, Ptr, hdc)
}


DeleteDC(hdc) {
    ; Deletes the specified device context (DC)
    ;
    ; An application must not delete a DC whose handle was obtained by calling
    ; the GetDC function. Instead, it must call the ReleaseDC function to free the DC.
    ;
    ; hdc		A handle to the device context.
    ;
    ; return	If the function succeeds, the return value is nonzero.
    return DllCall("DeleteDC", A_PtrSize ? "UPtr" : "UInt", hdc)
}


GetMonitorInfo(MonitorNum) {
    Monitors := MDMF_Enum()
    for k,v in Monitors
        if (v.Num = MonitorNum)
            return v
}


CreateRect(ByRef name, x, y, w, h) {
    ; Create a Rect object, containing a coordinates & dimensions of a rectangle
    ;
    ; name	    Name to call the RectF object
    ; x			x-coordinate of the upper left corner of the rectangle
    ; y			y-coordinate of the upper left corner of the rectangle
    ; w			Width of the rectangle
    ; h			Height of the rectangle
    ; return	No return value
    VarSetCapacity(name, 16)
    NumPut(x, name, 0, "uint")
    NumPut(y, name, 4, "uint")
    NumPut(w, name, 8, "uint")
    NumPut(h, name, 12, "uint")
}


CreateDIBSection(w, h, hdc:="", bpp:=32, ByRef ppvBits:=0) {
    ; Create a DIB (Device Independent Bitmap) that applications can write to directly.
    ;
    ; w			width of the bitmap to create
    ; h			height of the bitmap to create
    ; hdc		a handle to the device context to use the palette from
    ; bpp		bits per pixel (32 = ARGB)
    ; ppvBits	A pointer to a variable that receives a pointer to the location of
    ;           the DIB bit values. ppvBits will receive the location of pixels in the DIB.
    ; return	DIB. A gdi bitmap.
    Ptr := A_PtrSize ? "UPtr" : "UInt"

        hdc2 := hdc ? hdc : GetDC()
        VarSetCapacity(bi, 40, 0)

        NumPut(w, bi, 4, "uint")
        , NumPut(h, bi, 8, "uint")
        , NumPut(40, bi, 0, "uint")
        , NumPut(1, bi, 12, "ushort")
        , NumPut(0, bi, 16, "uInt")
        , NumPut(bpp, bi, 14, "ushort")

        hbm := DllCall("CreateDIBSection"
            , Ptr, hdc2
            , Ptr, &bi
            , "uint", 0
            , A_PtrSize ? "UPtr*" : "uint*", ppvBits
            , Ptr, 0
            , "uint", 0, Ptr)

        if !hdc
            ReleaseDC(hdc2)
    return hbm
}


BitBlt(ddc, dx, dy, dw, dh, sdc, sx, sy, Raster:="") {
    ; Perform a bit-block transfer of the color data corresponding to a rectangle.
    ; of pixels from the specified source device context into a destination device context.
    ;
    ; dDC					handle to destination DC
    ; dx					x-coord of destination upper-left corner
    ; dy					y-coord of destination upper-left corner
    ; dw					width of the area to copy
    ; dh					height of the area to copy
    ; sDC					handle to source DC
    ; sx					x-coordinate of source upper-left corner
    ; sy					y-coordinate of source upper-left corner
    ; Raster				raster operation code
    ;
    ; return				If the function succeeds, the return value is nonzero
    ;
    ; notes					If no raster operation is specified, then SRCCOPY is used, which copies the source directly to the destination rectangle
    ;
    ; BLACKNESS				= 0x00000042
    ; NOTSRCERASE			= 0x001100A6
    ; NOTSRCCOPY			= 0x00330008
    ; SRCERASE				= 0x00440328
    ; DSTINVERT				= 0x00550009
    ; PATINVERT				= 0x005A0049
    ; SRCINVERT				= 0x00660046
    ; SRCAND				= 0x008800C6
    ; MERGEPAINT			= 0x00BB0226
    ; MERGECOPY				= 0x00C000CA
    ; SRCCOPY				= 0x00CC0020
    ; SRCPAINT				= 0x00EE0086
    ; PATCOPY				= 0x00F00021
    ; PATPAINT				= 0x00FB0A09
    ; WHITENESS				= 0x00FF0062
    ; CAPTUREBLT			= 0x40000000
    ; NOMIRRORBITMAP		= 0x80000000
    Ptr := A_PtrSize ? "UPtr" : "UInt"
    return DllCall("gdi32\BitBlt"
        , Ptr, dDC
        , "int", dx, "int", dy
        , "int", dw, "int", dh
        , Ptr, sDC
        , "int", sx, "int", sy
        , "uint", Raster ? Raster : 0x00CC0020)
}


Gdip_Startup(multipleInstances:=0) {
    Static Ptr := "UPtr"
    pToken := 0
    If (multipleInstances=0) {
        If !DllCall("GetModuleHandle", "str", "gdiplus", Ptr)
            DllCall("LoadLibrary", "str", "gdiplus")
    } Else {
        DllCall("LoadLibrary", "str", "gdiplus")
    }

    VarSetCapacity(si, A_PtrSize = 8 ? 24 : 16, 0)
    si := Chr(1)
    DllCall("gdiplus\GdiplusStartup", "UPtr*", pToken, Ptr, &si, Ptr, 0)
    return pToken
}

Gdip_Shutdown(pToken) {
   Static Ptr := "UPtr"

   DllCall("gdiplus\GdiplusShutdown", Ptr, pToken)
   hModule := DllCall("GetModuleHandle", "str", "gdiplus", Ptr)
   if hModule
      DllCall("FreeLibrary", Ptr, hModule)
   return 0
}