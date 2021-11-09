from a2qt import QtWidgets
from singlesiding import QSingleApplication

class A2App(QSingleApplication):
    """The a2 app foundation object."""

    def __init__(self):
        super(A2App, self).__init__(list)
        self._app: QSingleApplication = ...
        self._win: QtWidgets.QMainWindow = ...
