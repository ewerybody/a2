import a2uic
from a2widget.demo import a2combo_demo_ui
from PySide6 import QtCore, QtWidgets

LIST_ITEMS = 'mango banana apple kiwi apple strawberry'.split()


class ComboDemo(QtWidgets.QMainWindow):
    dict_changed = QtCore.Signal(tuple)

    def __init__(self):
        super().__init__()
        a2uic.check_module(a2combo_demo_ui)
        self.ui = a2combo_demo_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        for i in range(1, 4):
            this_combo = getattr(self.ui, f'combo{i}')
            this_combo.addItems(LIST_ITEMS)
            this_combo = getattr(self.ui, f'a_combo{i}')
            this_combo.addItems(LIST_ITEMS)


def show():
    app = QtWidgets.QApplication([])
    win = ComboDemo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
