time_unix() {
    ; T := A_Now
    T := A_NowUTC
    T -= 19700101000000,seconds

    return T
}

time_unix_ms(decimals=2) {
    T := time_unix()
    T += A_MSec / 1000
    T := Round(T, decimals)
    return T
}
