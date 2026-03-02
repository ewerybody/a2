; LC_Version := "0.0.21.01"
; truncated version to what's currently fixed already for ahk2

/**
 * Decode a Base64-encoded string into a binary buffer.
 * Strips data-URI prefixes (e.g. "data:image/png;base64,") and whitespace before decoding.
 * @param {(String)} base64
 * Base64-encoded string to decode. May include a data-URI prefix.
 * @param {(Buffer)} &outBuf
 * Output buffer that will receive the decoded bytes.
 * @returns {(Integer)}
 * Number of bytes written to outBuf.
 */
LC_Base64ToBuf(base64, &outBuf) {
    ; remove optional data-uri prefix + whitespace/newlines
    base64 := RegExReplace(base64, "i)^data:[^;]+;base64,")
    base64 := RegExReplace(base64, "\s+")

    base64_length := StrLen(base64)
    if (base64_length = 0)
        throw Error("Base64 string is empty after cleanup.")

    pOutSize := Buffer(4, 0) ; DWORD pcbBinary

    ; size query
    ok := DllCall("Crypt32\CryptStringToBinaryW"
        , "Ptr", StrPtr(base64)
        , "UInt", base64_length
        , "UInt", 0x1
        , "Ptr", 0
        , "Ptr", pOutSize.Ptr
        , "Ptr", 0
        , "Ptr", 0
        , "Int")

    if !ok
        throw OSError()

    outLen := NumGet(pOutSize, 0, "UInt")
    if (outLen = 0)
        throw Error("LC_Base64ToBuf: Decoded length is 0. First8=" SubStr(base64, 1, 8) " Last8=" SubStr(base64, -8) " base64_length=" base64_length)

    outBuf := Buffer(outLen)

    ; decode
    NumPut("UInt", outLen, pOutSize, 0)
    ok := DllCall("Crypt32\CryptStringToBinaryW"
        , "Ptr", StrPtr(base64)
        , "UInt", base64_length
        , "UInt", 0x1
        , "Ptr", outBuf.Ptr
        , "Ptr", pOutSize.Ptr
        , "Ptr", 0
        , "Ptr", 0
        , "Int")

    if !ok
        throw OSError()

    return NumGet(pOutSize, 0, "UInt")
}