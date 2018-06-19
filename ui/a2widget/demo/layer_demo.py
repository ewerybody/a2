from PySide2 import QtCore, QtWidgets
from a2widget.demo import layer_demo_ui
import a2ctrl


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()

        a2ctrl.check_ui_module(layer_demo_ui)

        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QFormLayout(w)
        w.setLayout(lyt)

        self.lw = QtWidgets.QWidget(self)
        self.ui = layer_demo_ui.Ui_Form()
        self.ui.setupUi(self.lw)

        self.ui.layout_1.setAlignment(self.ui.toolButton, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.ui.gridLayout.addLayout(self.ui.layout_1, 0, 0)

        lyt.addRow('scope', self.lw)


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
