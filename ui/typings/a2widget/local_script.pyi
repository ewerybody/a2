import a2ui
from a2qt import QtCore, QtWidgets


class BrowseScriptsMenu(QtWidgets.QMenu):
    script_selected: QtCore.Signal

    file_prefix: str
    script_template: str
    config_typ: str
    dialog_title: str
    dialog_msg: str

    def __init__(self, parent: QtCore.QObject | None, main: a2ui.A2Window) -> None: ...
    def get_available_scripts(self) -> set[str]: ...

def build_file_name(name: str, prefix: str, extension: None | str = ...) -> str: ...