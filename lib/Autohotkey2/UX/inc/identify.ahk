#include identify_regex.ahk

IdentifyBySyntax(code) {
    static identify_regex := get_identify_regex()
    p := 1, count_1 := count_2 := 0, version := marks := ''
    while (p := RegExMatch(code, identify_regex, &m, p)) {
        p += m.Len()
        if SubStr(m.mark,1,1) = 'v' {
            switch SubStr(m.mark,2,1) {   
            case '1': count_1++
            case '2': count_2++
            }
            if !InStr(marks, m.mark)
                marks .= m.mark ' '
        }
    }
    if !(count_1 || count_2)
        return {v: 0, r: "no tell-tale matches"}
    ; Use a simple, cautious approach for now: select a version only if there were
    ; matches for exactly one version.
    if count_1 && count_2
        return {v: 0, r: Format(
            count_1 > count_2 ? "v1 {1}:{2} - {3}" : count_2 > count_1 ? "v2 {2}:{1} - {3}" : "? {1}:{2} - {3}",
            count_1, count_2, Trim(marks)
        )}
    return {v: count_1 ? 1 : 2, r: Trim(marks)}
}
