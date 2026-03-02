/**
 * Read a little-endian integer from a Buffer at a given byte offset.
 *
 * @sample
 *     buf := Buffer(4, 0)
 *     NumPut("UInt", 0x12345678, buf, 0)
 *     val := bytes_get_integer(buf, 0, false, 4)  ; val == 0x12345678
 *
 * @param {(Buffer)} pSource
 * Buffer object containing the raw binary data.
 * @param {(Integer)} pOffset
 * Byte offset within pSource where the integer starts. Defaults to 0.
 * @param {(Integer)} pIsSigned
 * Pass true to interpret the result as a signed integer. Defaults to false.
 * @param {(Integer)} pSize
 * Number of bytes to read (e.g. 2 for a Word/Short, 4 for a DWord/Int). Defaults to 4.
 * @returns {(Integer)}
 */
bytes_get_integer(pSource, pOffset := 0, pIsSigned := false, pSize := 4) {
    result := 0
    loop pSize ; Accumulate bytes, little-endian.
        result += NumGet(pSource, pOffset + A_Index - 1, "UChar") << 8 * (A_Index - 1)
    ; Return as-is if unsigned, larger than 32-bit, or high bit is clear (positive either way).
    if (!pIsSigned OR pSize > 4 OR result < 0x80000000)
        return result
    ; High bit is set on a 32-bit signed value — convert to its negative counterpart.
    return -(0xFFFFFFFF - result + 1)
}

/**
 * Format a file size in bytes to human-readable size string.
 *
 * @sample
 *     x := bytes_format(31236)
 *
 * @param {(Integer)} bytes
 * Number of bytes to be formatted.
 * @param {(Integer)} decimals
 * Number of decimals to be shown.
 * @returns {(String)}
 */
bytes_format(bytes, decimals := 1) {
    suffixes := "B,KB,MB,GB,TB,PB,EB,ZB,YB"
    loop Parse, suffixes, "," {
        if (bytes < e := 1024 ** A_Index)
            return Round(bytes / (e / 1024), decimals) . A_LoopField
    }
}
