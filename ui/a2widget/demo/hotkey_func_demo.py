from pprint import pprint

from a2qt import QtWidgets

import a2uic
import a2ctrl
from a2widget.a2hotkey import edit_func_widget, edit_func_widget_ui


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()

        a2uic.check_module(edit_func_widget_ui)

        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        # lyt = QtGui.QVBoxLayout(w)
        lyt = QtWidgets.QFormLayout(w)
        w.setLayout(lyt)

        self.cfg = {
            'name': '_my_module_Hotkey2',
            'functionCode': 'calculAid_open()',
            'functionMode': 2,
            'functionSend': '',
            'functionURL': '',
        }

        self.func_widget = edit_func_widget.FuncWidget(self)
        a2ctrl.connect.cfg_controls(self.cfg, self.func_widget.ui)
        self.func_widget.set_config(self.cfg)
        self.func_widget.changed.connect(self.bla)
        lyt.addRow('function', self.func_widget)

        # self.scope_widget.changed.connect(self.bla)

        button = QtWidgets.QPushButton('set_config')
        button.clicked.connect(self.bla)
        lyt.addRow(button)

        # self.scope_widget.ui.cfg_scopeChange.clicked.connect(self.bla)
        # self.scope_widget.ui.cfg_scopeMode.currentIndexChanged.connect(self.bla)

    def bla(self):
        print('id(self.cfg): %s' % id(self.cfg))
        pprint(self.cfg)


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
