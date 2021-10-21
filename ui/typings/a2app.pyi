import typing
from singlesiding import QSingleApplication
from a2qt import QtWidgets

class A2App(QSingleApplication):
    """The a2 app foundation object."""

    def __init__(self):
        super(A2App, self).__init__(list)
        self._app: typing.Optional[QSingleApplication] = None
        self._win: typing.Optional[QtWidgets.QMainWindow] = None
