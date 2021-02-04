import typing
from singlesiding import QSingleApplication
from a2qt import QtWidgets

class A2Main(QSingleApplication):
    """The a2 app foundation object."""

    def __init__(self):
        super(A2Main, self).__init__(list)
        self._app: typing.Optional[QSingleApplication] = None
        self._win: typing.Optional[QtWidgets.QMainWindow] = None
