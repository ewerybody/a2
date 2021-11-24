from a2qt import QtGui

class Ico(QtGui.QIcon):
    @property
    def tinted(self) -> QtGui.QIcon: ...

class LibIco(Ico): ...

class _Icons:
    a2: Ico
    a2help: Ico
    a2reload: Ico
    a2tinted: Ico
    a2x: Ico
    autohotkey: Ico
    github: Ico

    button: LibIco
    check: LibIco
    check_circle: LibIco
    clear: LibIco
    cloud_download: LibIco
    code: LibIco
    combo: LibIco
    copy: LibIco
    cut: LibIco
    delete: LibIco
    down: LibIco
    down_align: LibIco
    down_circle: LibIco
    edit: LibIco
    error: LibIco
    file_download: LibIco
    folder: LibIco
    folder2: LibIco
    folder_add: LibIco
    group: LibIco
    help: LibIco
    keyboard: LibIco
    label: LibIco
    label_plus: LibIco
    list_add: LibIco
    locate: LibIco
    more: LibIco
    number: LibIco
    paste: LibIco
    reload: LibIco
    rollback: LibIco
    scope: LibIco
    scope_exclude: LibIco
    scope_global: LibIco
    string: LibIco
    text: LibIco
    up: LibIco
    up_align: LibIco

Icons: _Icons

def get(current_icon: QtGui.QIcon | None, folder: str, fallback=None) -> QtGui.QIcon: ...
