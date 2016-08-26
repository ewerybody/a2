set Ahk2Exe="C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set script=..\..\a2ui
set icon=..\..\ui\res\a2.ico
%Ahk2Exe% /in %script%.ahk /out %script%.exe /icon %icon% /mpress 1
