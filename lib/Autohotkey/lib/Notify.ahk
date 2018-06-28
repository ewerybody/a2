Notify(Title, Text, Timeout = "", Icon = "", Action = "", Progress = "", Style = "")
{
    if ((WinVer < Win_10) OR (Actione != "") OR (Progress != "") OR (Style != ""))
        return new CNotificationWindow(Title, Text, Icon, Timeout, Action, Progress, Style)
    else {
        if (Timeout > 30)   ; TrayTip has a max value of 30 seconds
            Timeout := 30   ; For longer TrayTip, the module has to handle it with a timer
        if ((Timeout == "") OR (!(IsNumeric(Timeout))))
            Timeout := 5   ; fallback to a default value

        _icon := 0
        if (Icon == NotifyIcons.Info)
            _icon := _icon + 1 + 32
        if (Icon == NotifyIcons.Warning)
            _icon := _icon + 2 + 32
        if (Icon == NotifyIcons.Error)
            _icon := _icon + 3 + 32
        TrayTip, % Title, % Text, % Timeout, % _icon
    }
}