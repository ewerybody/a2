; LC_Version := "0.0.21.01"
; truncated version to what's currently fixed already for ahk2

LC_Str2Bin(&Out, &Inn, Flags)
{
	DllCall("Crypt32.dll\CryptStringToBinary", "Ptr", &Inn, "UInt", StrLen(Inn)
	, "UInt", Flags, "Ptr", 0, "UInt*", &OutLen, "Ptr", 0, "Ptr", 0)
	VarSetStrCapacity(&Out, OutLen)
	DllCall("Crypt32.dll\CryptStringToBinary", "Ptr", &Inn, "UInt", StrLen(Inn)
	, "UInt", Flags, "Str", Out, "UInt*", OutLen, "Ptr", 0, "Ptr", 0)
	return OutLen
}
