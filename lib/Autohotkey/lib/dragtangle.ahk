; Rectangle area selection tool.
; You pass it function names for events you're interested in,
; it calls the functions with a data object about the current rectangle.
;
; The event functions:
; * drag_func:     fires while dragging
; * start_func:    fires on first mouse button down
; * finished_func: fires when mouse button is released
; * escape_func:   fires when Escape is pressed and the loop is broken
; other arguments:
; * loop_delay:    milliseconds of sleep between evaluations.
; * data:          To pass a predefined data object.

dragtangle(drag_func := ""
, start_func := "", finished_func := ""
, escape_func := "", loop_delay := 20, data := "")
{
    if (!IsObject(data))
        data := {}
    data.started := false

    cursor_set_cross()
    CoordMode, Mouse, Screen

    Loop
    {
        if (GetKeyState("Escape", "p") == "D") {
            if IsFunc(escape_func)
                %escape_func%(data)
            cursor_reset()
            Return data
        }

        MouseGetPos, mx, my
        data.mx := mx
        data.my := my

        if (GetKeyState("LButton", "p") == "D") {
            if (!data.started) {
                data.started := true
                data.start_x := mx
                data.start_y := my
                if IsFunc(start_func)
                    %start_func%(data)
            } else {
                data.w := Abs(data.start_x - mx)
                data.h := Abs(data.start_y - my)
                data.x := min(data.start_x, mx)
                data.y := min(data.start_y, my)
                data.x2 := data.x + data.w
                data.y2 := data.y + data.h
                data.dist := Sqrt(data.w**2 + data.h**2)
                if IsFunc(drag_func)
                    %drag_func%(data)
            }
        } else if (data.started) {
            if IsFunc(finished_func)
                %finished_func%(data)
            cursor_reset()
            Return data
        }
        Sleep, %loop_delay%
    }

    Return data
}
