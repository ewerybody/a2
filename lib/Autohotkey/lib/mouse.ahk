mouse_wheel_delta(value, mousex := "", mousey := "", win_id := "", modifiers := "") {
    ; Send NON-page-wise wheel rotations.
    ; Note: +/- 120 seems to be the "default" scroll.
    ; Linear Spoon posted about this ages ago:
    ; https://autohotkey.com/board/topic/119433-how-to-send-a-smooth-scroll-signal/?p=681249
    ; with this WIN api link:
    ; http://msdn.microsoft.com/en-us/library/windows/desktop/ms645617(v=vs.85).aspx
    ;
    ; To use this the key is to send the according modifiers along right away
    ; AND make sure that interfering modifiers are not pressed anymore. Liek `Send {Shift Up}`

    if (mousex == "")
        MouseGetPos &mouse_x1, &mouse_y1, &_mouse_win_id

    if (win_id == "") {
        if (_mouse_win_id != "")
            win_id := _mouse_win_id
        else
            MouseGetPos ,, &win_id
    }

    if (modifiers == "") {
        modifiers := 0x8*GetKeyState("ctrl") | 0x1*GetKeyState("lbutton") | 0x10*GetKeyState("mbutton")
                  |0x2*GetKeyState("rbutton") | 0x4*GetKeyState("shift") | 0x20*GetKeyState("xbutton1")
                  |0x40*GetKeyState("xbutton2")
    }

    wparam := value << 16 | modifiers
    lparam := mousey << 16 | mousex
    PostMessage 0x20A, wparam, lparam ,, "ahk_id " . win_id
}
