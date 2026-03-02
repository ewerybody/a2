#Requires AutoHotkey v2.0
#Include <time>

class TimeTests {
    class Unix {
        returns_positive_number() {
            t := time_unix()
            if t <= 0
                throw Error("time_unix should return positive, got " t)
        }

        after_year_2020() {
            ; 2020-01-01 00:00:00 UTC = 1577836800
            t := time_unix()
            if t <= 1577836800
                throw Error("time_unix should be after 2020, got " t)
        }

        before_year_2100() {
            ; 2100-01-01 00:00:00 UTC = 4102444800
            t := time_unix()
            if t >= 4102444800
                throw Error("time_unix should be before 2100, got " t)
        }
    }

    class UnixMs {
        not_less_than_unix() {
            t := time_unix()
            t_ms := time_unix_ms()
            if t_ms < t
                throw Error("time_unix_ms (" t_ms ") should be >= time_unix (" t ")")
        }

        zero_decimals_is_integer() {
            t := time_unix_ms(0)
            if t != Integer(t)
                throw Error("time_unix_ms(0) should be integer-valued, got " t)
        }

        positive_value() {
            t := time_unix_ms()
            if t <= 0
                throw Error("time_unix_ms should be positive, got " t)
        }
    }
}
