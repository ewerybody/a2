import typing
from a2qt import QtCore, QtWidgets

class A2ConfirmDialog(QtWidgets.QDialog):
    okayed: QtCore.Signal = ...
    canceled: QtCore.Signal = ...
    def __init__(
        self,
        parent: QtCore.QObject,
        title: str,
        msg: str = '',
        ok_func: typing.Callable = None,
    ) -> None: ...

class A2InputDialog(A2ConfirmDialog):
    field_changed: QtCore.Signal = ...
    output: str
    def __init__(
        self,
        parent: QtCore.QObject | None = ...,
        title: str = ...,
        check_func: typing.Callable | None = ...,
        text: str = ...,
        msg: str = ...,
        ok_func: typing.Callable | None = ...,
    ) -> None: ...
    class ui:
        main_layout: QtWidgets.QHBoxLayout
        label: QtWidgets.QLabel