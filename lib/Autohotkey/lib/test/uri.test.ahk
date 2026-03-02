#Requires AutoHotkey v2.0
#Include <uri>

class Encode {
    colon_becomes_percent3A() {
        result := uri_encode(":")
        if result != "%3A"
            throw Error("Expected '%3A', got '" result "'")
    }

    slash_becomes_percent2F() {
        result := uri_encode("/")
        if result != "%2F"
            throw Error("Expected '%2F', got '" result "'")
    }

    space_becomes_percent20() {
        result := uri_encode(" ")
        if result != "%20"
            throw Error("Expected '%20', got '" result "'")
    }

    alphanumeric_is_unchanged() {
        s := "abc123"
        result := uri_encode(s)
        if result != s
            throw Error("Expected '" s "', got '" result "'")
    }

    linebreak_is_encoded() {
        result := uri_encode("`n")
        if !InStr(result, "%")
            throw Error("Linebreak should be percent-encoded, got '" result "'")
    }

    custom_safe_chars_preserved() {
        ; With custom RE keeping ":", colon should not be encoded
        result := uri_encode("a:b", "[0-9a-zA-Z:]")
        if result != "a:b"
            throw Error("Colon should be preserved with custom RE, got '" result "'")
    }
}

class Decode {
    percent3A_becomes_colon() {
        result := uri_decode("%3A")
        if result != ":"
            throw Error("Expected ':', got '" result "'")
    }

    percent2F_becomes_slash() {
        result := uri_decode("%2F")
        if result != "/"
            throw Error("Expected '/', got '" result "'")
    }

    plain_string_is_unchanged() {
        s := "hello"
        result := uri_decode(s)
        if result != s
            throw Error("Expected '" s "', got '" result "'")
    }

    lowercase_hex_is_decoded() {
        result := uri_decode("%3a")
        if result != ":"
            throw Error("Lowercase hex should decode, got '" result "'")
    }
}

class RoundTrip {
    encode_decode_restores_original() {
        original := "https://example.com/path?q=hello world&r=2"
        encoded := uri_encode(original)
        decoded := uri_decode(encoded)
        if decoded != original
            throw Error("Round-trip failed: got '" decoded "'")
    }
}

class UrlEncode {
    keeps_scheme_and_slashes() {
        url := "https://example.com/foo"
        result := uri_url_encode(url)
        if InStr(result, "%3A") || InStr(result, "%2F")
            throw Error("uri_url_encode should keep :// intact, got '" result "'")
    }

    encodes_spaces() {
        result := uri_url_encode("hello world")
        if !InStr(result, "%20")
            throw Error("uri_url_encode should encode spaces, got '" result "'")
    }

    round_trip_restores_url() {
        original := "https://example.com/contact/rf/contact.jsp"
        encoded := uri_url_encode(original)
        decoded := uri_decode(encoded)
        if decoded != original
            throw Error("url_encode round-trip failed: got '" decoded "'")
    }
}
