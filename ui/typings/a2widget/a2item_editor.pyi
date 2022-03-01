import types, typing
from a2qt import QtWidgets, QtCore


class A2ItemEditor(QtWidgets.QWidget):
    def add_data_widget(
        self,
        value_name: str,
        widget: QtWidgets.QWidget,
        set_function: types.FunctionType,
        change_signal: QtCore.Signal,
        default_value=typing.Any
    ):
        pass

    def add_data_label_widget(
        self,
        value_name: str,
        widget: QtWidgets.QWidget,
        set_function: types.FunctionType,
        change_signal: QtCore.Signal,
        default_value: typing.Any,
        label: str = ...
    ):
        pass