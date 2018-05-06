from PySide import QtGui
from a2widget.a2hotkey import edit_scope_widget, edit_scope_widget_ui
import a2ctrl
from pprint import pprint


class Demo(QtGui.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()

        a2ctrl.check_ui_module(edit_scope_widget_ui)

        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtGui.QFormLayout(w)
        w.setLayout(lyt)

        self.cfg = {"name": "_my_module_Hotkey2",
                    "scope": ["WhatsApp - Mozilla Firefox ahk_exe firefox.exe"],
                    "scopeChange": False,
                    "scopeMode": 1}

        self.scope_widget = edit_scope_widget.ScopeWidget(self)
        lyt.addRow('scope', self.scope_widget)

        a2ctrl.connect.cfg_controls(self.cfg, self.scope_widget.ui)
        self.scope_widget.changed.connect(self.bla)

        button = QtGui.QPushButton('set_config')
        button.clicked.connect(self.bla)
        lyt.addRow(button)

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
