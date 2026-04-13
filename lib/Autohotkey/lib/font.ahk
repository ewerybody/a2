/**
 * Create a font and set it to a given Window handle.
 * from http://www.autohotkey.com/forum/viewtopic.php?p=124450#124450
 * @example
 * font_set(win_id, "s12 bold, Courier New")
 * font_set(win_id, "s12 bold, Comic Sans MS")
 * @param {(Integer)} win_id - Handle of the window to set the font.
 * @param {(String)} font_params - Font setting string.
 * @author majkinetor
 */
font_set(win_id, font_params) {
    h_font := font_make(font_params)
    font_apply(h_font, win_id)
}

/**
 * Take font describing string, disassemble it and pass it to `CreateFont` to get handle.
 * @param {(String)} font_params - String describing the font to use. Specifically thats:
 * - `s` for size followed by an integer e.g. "s12"
 * - any of the keywords `italic`, `underline`, `strikeout`, `bold`
 * - a comma and
 * - the exact Font name e.g. "Comic Sans MS" (instead of just 'Comic Sans')
 * @returns {(Integer)}  handle of the font
 */
font_make(font_params) {
    ;parse the font
    italic := InStr(font_params, "italic") ? 1 : 0
    underline := InStr(font_params, "underline") ? 1 : 0
    strikeout := InStr(font_params, "strikeout") ? 1 : 0
    weight := InStr(font_params, "bold") ? 700 : 400
    n_char_set := 0

    ; calculate height
    if RegExMatch(font_params, "(?<=[Ss])(\d{1,2})(?=[ ,])", &height)
        height := height[1]
    else
        height := 10
    height := _font_height_from_size(height)

    ; get the font face
    if RegExMatch(font_params, "(?<=,).+", &font_face)
        font_face := Trim(font_face[0])
    else
        font_face := "MS Sans Serif"
    ; create font
    h_font := DllCall("CreateFont", "int", height, "int", 0, "int", 0, "int", 0,
        "int", weight, "uint", italic, "uint", underline, "uint", strikeOut,
        "uint", n_char_set, "uint", 0, "uint", 0, "uint", 0, "uint", 0, "str", font_face
    )

    if !h_font
        throw Error('CreateFont failed for: "' font_face '" - Error: ' A_LastError)

    return h_font
}

/**
 * Use `SendMessage` to apply font to window handle.
 * @param {(Integer)} h_font - Handle of the font.
 * @param {(Integer)} win_id - Window handle to apply the font to.
 */
font_apply(h_font, win_id) {
    static WM_SetFont := 0x30
    if win_id == 0
        return
    SendMessage(WM_SetFont, h_font, false,, "ahk_id " win_id)
}

/**
 * Pop a font selection dialog and get back object with selected props.
 * @param {(Integer)} owner - Window handle to make the font selection dialog a modal child of.
 * @param {(Object)} [current] - Object with font props: `face` - Name of the font.
 * Optional: `size` - Font size. `bold` - Font weight. `italic` - slanted font.
 * @returns {(Object)}  {face: {(String)}, size: {(Integer)}, bold: {(Boolean)}}
 */
font_pick(owner := 0, current := "") {
    static CF_SCREEN_FONTS := 0x01
    static CF_INIT_TO_LOG_FONT_STRUCT := 0x40

    lf := Buffer(92, 0) ; LOG_FONT struct (92 bytes on x64)
    ; pre-fill if current font provided
    if current != "" {
        height := _font_height_from_size(current.HasProp('size') ? current.size : 10)
        NumPut("int", height, lf, 0)
        NumPut("int", current.HasProp('bold') && current.bold ? 700 : 400, lf, 16)
        NumPut("uint", current.HasProp('italic') && current.italic ? 1 : 0, lf, 20)
        StrPut(current.face, lf.Ptr + 28, 32, "UTF-16")
    }

    cf := Buffer(104, 0) ; CHOOSE_FONT on x64
    NumPut("uint", 104, cf, 0) ; lStructSize
    NumPut("ptr", owner, cf, 8) ; hwndOwner
    NumPut("ptr", lf.Ptr, cf, 24) ; lpLogFont
    NumPut("uint", CF_SCREEN_FONTS | CF_INIT_TO_LOG_FONT_STRUCT, cf, 36)  ; Flags

    if !DllCall("ComDlg32\ChooseFontW", "ptr", cf)
        return ""

    ; lfFaceName at offset 28, max 32 chars
    face := StrGet(lf.Ptr + 28, 32, "UTF-16")
    ; iPointSize (in 1/10 points)
    height := NumGet(cf, 32, "int")
    ; lfWeight
    weight := NumGet(lf, 16, "int")
    return { face: face, size: height // 10, bold: weight >= 700 }
}


_font_height_from_size(size) {
    log_pixels := RegRead("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontDPI", "LogPixels")
    return -DllCall("MulDiv", "int", size, "int", log_pixels, "int", 72)
}
