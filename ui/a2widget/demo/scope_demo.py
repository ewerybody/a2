from PySide import QtGui
from a2widget.a2hotkey.edit_scope_widget import ScopeWidget
import a2ctrl
from pprint import pprint


class Demo(QtGui.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtGui.QVBoxLayout(w)
        w.setLayout(lyt)

        self.cfg = {"name": "_my_module_Hotkey2",
                    "scope": ["WhatsApp - Mozilla Firefox ahk_exe firefox.exe"],
                    "scopeChange": False,
                    "scopeMode": 1}

        self.scope_widget = ScopeWidget(self)
        lyt.addWidget(self.scope_widget)

        self.scope_widget.changed.connect(self.bla)

        a2ctrl.connect.cfg_controls(self.cfg, self.scope_widget.ui)

        button = QtGui.QPushButton('set_config')
        button.clicked.connect(self.bla)
        lyt.addWidget(button)

        self.scope_widget.ui.cfg_scopeChange.clicked.connect(self.bla)
        self.scope_widget.ui.cfg_scopeMode.currentIndexChanged.connect(self.bla)

    def bla(self):
        pprint(self.cfg)


def show():
    app = QtGui.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
