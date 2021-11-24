import a2ui
import a2modsource
from a2qt import QtWidgets, QtCore


class EditView(QtWidgets.QWidget):
    mod_source: a2modsource.ModSource
    okayed: QtCore.Signal

    def __init__(self, parent: a2ui.A2Window) -> None: ...
    def get_cfg_copy(self) -> dict: ...
    def check_issues(self) -> list[dict]: ...
