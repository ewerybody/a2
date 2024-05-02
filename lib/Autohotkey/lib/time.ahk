; Support for Unix or epoch time stamps for straight forward comparison
; with other languages and systems. https://en.wikipedia.org/wiki/Unix_time

; Tell current time in seconds.
time_unix() {
    ; T := A_Now
    Return DateDiff("", 19700101000000, "seconds")
}

; Tell current time in miliseconds.
time_unix_ms(decimals:=2) {
    T := time_unix()
    T += A_MSec / 1000
    T := Round(T, decimals)
    return T
}
