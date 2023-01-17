; From Gdip_All.ahk - The GDI+ library compilation of user contributed GDI+ functions
; made by Marius Șucan: https://github.com/marius-sucan/AHK-GDIp-Library-Compilation

gdip_startup(multipleInstances:=0) {
   Static Ptr := "UPtr"
   pToken := 0
   If (multipleInstances=0)
   {
      if !DllCall("GetModuleHandle", "str", "gdiplus", Ptr)
         DllCall("LoadLibrary", "str", "gdiplus")
   } Else DllCall("LoadLibrary", "str", "gdiplus")

   VarSetCapacity(si, A_PtrSize = 8 ? 24 : 16, 0), si := Chr(1)
   DllCall("gdiplus\GdiplusStartup", "UPtr*", pToken, Ptr, &si, Ptr, 0)
   return pToken
}


gdip_shutdown(pToken) {
   Static Ptr := "UPtr"

   DllCall("gdiplus\GdiplusShutdown", Ptr, pToken)
   hModule := DllCall("GetModuleHandle", "str", "gdiplus", Ptr)
   if hModule
      DllCall("FreeLibrary", Ptr, hModule)
   return 0
}


gdip_disposeimage(pBitmap, noErr:=0) {
    ; modified by Marius Șucan to help avoid crashes
    ; by disposing a non-existent pBitmap

    If (StrLen(pBitmap)<=2 && noErr=1)
        Return 0

    r := DllCall("gdiplus\GdipDisposeImage", "UPtr", pBitmap)
    If (r=2 || r=1) && (noErr=1)
        r := 0
    Return r
}


gdip_graphicsfromhdc(hdc) {
    ; Get graphics from handle to a device context.
    ; Return pointer to the graphics of a bitmap.
    ; note:	You can draw a bitmap into the graphics of another bitmap.
    ;
    ; hdc   Handle to the device context.
	pGraphics := 0

	DllCall("gdiplus\GdipCreateFromHDC"
    , A_PtrSize ? "UPtr" : "UInt", hdc
    , A_PtrSize ? "UPtr*" : "UInt*", pGraphics)
	return pGraphics
}


gdip_drawimage(pGraphics, pBitmap, dx:="", dy:="", dw:="", dh:="", sx:="", sy:="", sw:="", sh:="", Matrix:=1) {
    ; Draw a bitmap into the Graphics of another bitmap.
    ;
    ; pGraphics		Pointer to Graphics of a bitmap.
    ; pBitmap		Pointer to a bitmap to be drawn.
    ; dx, dy		x,y-coordinates of destination upper-left corner.
    ; dw, dh		width,height of destination image.
    ; sx,sy			x,z-coordinate of source upper-left corner.
    ; sw,sh			width,height of source image.
    ; Matrix		a matrix used to alter image attributes when drawing
    ;
    ; return		status enumeration. 0 = success
    ; notes			if sx,sy,sw,sh are missed then the entire source bitmap will be used
    ;				Gdip_DrawImage performs faster
    ;				Matrix can be omitted to just draw with no alteration to ARGB
    ;				Matrix may be passed as a digit from 0 - 1 to change just transparency
    ;				Matrix can be passed as a matrix with any delimiter. For example:
    ;				MatrixBright=
    ;				(
    ;				1.5		|0		|0		|0		|0
    ;				0		|1.5	|0		|0		|0
    ;				0		|0		|1.5	|0		|0
    ;				0		|0		|0		|1		|0
    ;				0.05	|0.05	|0.05	|0		|1
    ;				)
    ; notes			MatrixBright = 1.5|0|0|0|0|0|1.5|0|0|0|0|0|1.5|0|0|0|0|0|1|0|0.05|0.05|0.05|0|1
    ;				MatrixGreyScale = 0.299|0.299|0.299|0|0|0.587|0.587|0.587|0|0|0.114|0.114|0.114|0|0|0|0|0|1|0|0|0|0|0|1
    ;				MatrixNegative = -1|0|0|0|0|0|-1|0|0|0|0|0|-1|0|0|0|0|0|1|0|1|1|1|0|1

    Ptr := A_PtrSize ? "UPtr" : "UInt"

	if !IsNumber(Matrix)
		ImageAttr := Gdip_SetImageAttributesColorMatrix(Matrix)
	else if (Matrix != 1)
		ImageAttr := Gdip_SetImageAttributesColorMatrix("1|0|0|0|0|0|1|0|0|0|0|0|1|0|0|0|0|0|" Matrix "|0|0|0|0|0|1")

	if (sx = "" && sy = "" && sw = "" && sh = "")
	{
		if (dx = "" && dy = "" && dw = "" && dh = "")
		{
			sx := dx := 0, sy := dy := 0
			sw := dw := Gdip_GetImageWidth(pBitmap)
			sh := dh := Gdip_GetImageHeight(pBitmap)
		}
		else
		{
			sx := sy := 0
			sw := Gdip_GetImageWidth(pBitmap)
			sh := Gdip_GetImageHeight(pBitmap)
		}
	}

	_E := DllCall("gdiplus\GdipDrawImageRectRect"
    	, Ptr, pGraphics
    	, Ptr, pBitmap
    	, "float", dx , "float", dy
    	, "float", dw , "float", dh
    	, "float", sx , "float", sy
    	, "float", sw, "float", sh
    	, "int", 2
    	, Ptr, ImageAttr ? ImageAttr : 0
    	, Ptr, 0, Ptr, 0)
	if ImageAttr
		Gdip_DisposeImageAttributes(ImageAttr)
	return _E
}


gdip_SetImageAttributesColorMatrix(Matrix) {
    ; Create image matrix ready for drawing.
    ; Return image matrix on sucess or 0 if it fails
    ;
    ; Matrix	a matrix used to alter image attributes when drawing
    ;			passed with any delimeter
    ; notes		MatrixBright = 1.5|0|0|0|0|0|1.5|0|0|0|0|0|1.5|0|0|0|0|0|1|0|0.05|0.05|0.05|0|1
    ;			MatrixGreyScale = 0.299|0.299|0.299|0|0|0.587|0.587|0.587|0|0|0.114|0.114|0.114|0|0|0|0|0|1|0|0|0|0|0|1
    ;			MatrixNegative = -1|0|0|0|0|0|-1|0|0|0|0|0|-1|0|0|0|0|0|1|0|1|1|1|0|1

	Ptr := A_PtrSize ? "UPtr" : "UInt"
	ImageAttr := 0
	VarSetCapacity(ColourMatrix, 100, 0)
	Matrix := RegExReplace(RegExReplace(Matrix, "^[^\d-\.]+([\d\.])", "$1", , 1), "[^\d-\.]+", "|")
	Matrix := StrSplit(Matrix, "|")
	Loop 25
	{
		M := (Matrix[A_Index] != "") ? Matrix[A_Index] : Mod(A_Index-1, 6) ? 0 : 1
		NumPut(M, ColourMatrix, (A_Index-1)*4, "float")
	}
	DllCall("gdiplus\GdipCreateImageAttributes", A_PtrSize ? "UPtr*" : "uint*", ImageAttr)
	DllCall("gdiplus\GdipSetImageAttributesColorMatrix"
    , Ptr, ImageAttr, "int", 1, "int", 1
    , Ptr, &ColourMatrix, Ptr, 0, "int", 0)
	return ImageAttr
}



gdip_disposeImageAttributes(ImageAttr) {
	return DllCall("gdiplus\GdipDisposeImageAttributes", A_PtrSize ? "UPtr" : "UInt", ImageAttr)
}


gdip_GetImageWidth(pBitmap) {
    ; Return the width in pixels of the supplied bitmap pointer.
	Width := 0
	DllCall("gdiplus\GdipGetImageWidth", A_PtrSize ? "UPtr" : "UInt", pBitmap, "uint*", Width)
	return Width
}


gdip_GetImageHeight(pBitmap) {
    ; Return height in pixels of the supplied bitmap pointer.
	Height := 0
	DllCall("gdiplus\GdipGetImageHeight", A_PtrSize ? "UPtr" : "UInt", pBitmap, "uint*", Height)
	return Height
}


gdip_DeleteGraphics(pGraphics) {
   If pGraphics
      return DllCall("gdiplus\GdipDeleteGraphics", "UPtr", pGraphics)
}