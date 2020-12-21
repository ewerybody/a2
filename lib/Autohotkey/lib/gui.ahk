/**
 * Return a free identifier for a GUI.
 * v0.81 by majkinetor  Licenced under BSD <http://creativecommons.org/licenses/BSD/>
 *
 * @sample ; returns the first integer that is not used by a GUI
 *     gui_get_free_id(0)
 * @sample ; returns "Foo10" or the next higher integer that is not used by a GUI
 *     gui_get_free_id(10, "Foo")
 *
 * @param   integer     start   Number from where to start counting up
 * @param   string      prefix  String to help the GUI identifier to be unique
 * @return  string
 */
gui_get_free_id(start, prefix = ""){
    loop
    {
        Gui %prefix%%start%:+LastFoundExist
        IfWinNotExist
            return prefix start
        start++
        if (start = 100)
            return 0
    }
    return 0
}