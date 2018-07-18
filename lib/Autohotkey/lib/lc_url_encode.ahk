; Source: https://github.com/ahkscript/libcrypt.ahk/blob/master/src/URI.ahk
; Modified by GeekDude from http://goo.gl/0a0iJq
lc_url_encode(Url) { ; keep ":/;?@,&=+$#."
    return lc_uri_encode(Url, "[0-9a-zA-Z:/;?@,&=+$#.]")
}
