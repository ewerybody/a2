#Requires AutoHotkey v2.0
#Include <bytes>

class GetInteger {
    single_byte() {
        buf := Buffer(1, 0)
        NumPut("UChar", 200, buf, 0)
        result := bytes_get_integer(buf, 0, false, 1)
        if (result != 200)
            throw Error("Expected 200, got " result)
    }

    little_endian_dword() {
        ; 0x12345678 in little-endian: 78 56 34 12
        buf := Buffer(4, 0)
        NumPut("UChar", 0x78, buf, 0)
        NumPut("UChar", 0x56, buf, 1)
        NumPut("UChar", 0x34, buf, 2)
        NumPut("UChar", 0x12, buf, 3)
        result := bytes_get_integer(buf, 0, false, 4)
        if (result != 0x12345678)
            throw Error("Expected 0x12345678 (" 0x12345678 "), got " result)
    }

    reads_with_offset() {
        ; First 2 bytes are junk, then 0x00000005 at offset 2
        buf := Buffer(6, 0)
        NumPut("UChar", 0xFF, buf, 0)
        NumPut("UChar", 0xFF, buf, 1)
        NumPut("UChar", 0x05, buf, 2)
        result := bytes_get_integer(buf, 2, false, 4)
        if (result != 5)
            throw Error("Expected 5, got " result)
    }

    signed_minus_one() {
        ; 0xFFFFFFFF = -1 as signed 32-bit
        buf := Buffer(4, 0xFF)
        result := bytes_get_integer(buf, 0, true, 4)
        if (result != -1)
            throw Error("Expected -1 (signed), got " result)
    }

    unsigned_high_bit_stays_positive() {
        ; 0x80000000 unsigned should not be treated as negative
        buf := Buffer(4, 0)
        NumPut("UChar", 0x00, buf, 0)
        NumPut("UChar", 0x00, buf, 1)
        NumPut("UChar", 0x00, buf, 2)
        NumPut("UChar", 0x80, buf, 3)
        result := bytes_get_integer(buf, 0, false, 4)
        if (result != 0x80000000)
            throw Error("Expected " 0x80000000 ", got " result)
    }

    word_two_bytes() {
        buf := Buffer(2, 0)
        NumPut("UChar", 0x34, buf, 0)
        NumPut("UChar", 0x12, buf, 1)
        result := bytes_get_integer(buf, 0, false, 2)
        if (result != 0x1234)
            throw Error("Expected 0x1234 (" 0x1234 "), got " result)
    }
}

class FormatBytes {
    byte_range() {
        result := bytes_format(512)
        if (!InStr(result, "B") || InStr(result, "KB"))
            throw Error("512 should format as bytes, got '" result "'")
    }

    kilobytes_fractional() {
        result := bytes_format(1536)
        if (result != "1.5KB")
            throw Error("Expected '1.5KB', got '" result "'")
    }

    megabytes_fractional() {
        result := bytes_format(1536 * 1024)
        if (result != "1.5MB")
            throw Error("Expected '1.5MB', got '" result "'")
    }

    decimal_precision() {
        result := bytes_format(1536, 2)
        if (result != "1.50KB")
            throw Error("Expected '1.50KB', got '" result "'")
    }

    zero_decimals() {
        result := bytes_format(2 * 1024, 0)
        if (result != "2KB")
            throw Error("Expected '2KB', got '" result "'")
    }

    gigabytes() {
        result := bytes_format(1024 ** 3)
        if (!InStr(result, "GB"))
            throw Error("Expected GB suffix, got '" result "'")
    }
}
