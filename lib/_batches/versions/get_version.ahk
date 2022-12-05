path := A_Args[1]
if (!FileExist(path)) {
    MsgBox, No File found here`n%path%
    ExitApp
}

FileGetVersion, version, %path%
if (!version) {
    MsgBox, No version found!`n%path%
    ExitApp
}

FileAppend, %version%, *
