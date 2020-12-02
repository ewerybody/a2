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
