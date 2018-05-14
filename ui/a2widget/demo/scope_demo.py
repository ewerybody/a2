from pprint import pprint
from PySide import QtGui

import a2ctrl
from a2widget.a2hotkey import scope_widget, scope_widget_ui


config = {"typ": "hotkey",
          "name": "_my_module_Hotkey2",
          "label": "Standard Hotkey",
          "enabled": True,
          "disablable": True,
          "scope": ["WhatsApp - Mozilla Firefox ahk_exe firefox.exe"],
          "scopeMode": 1,
          "scopeChange": False,
          "functionCode": "calculAid_open()",
          "functionMode": 0,
          "functionSend": "",
          "functionURL": "",
          "key": "Ctrl+Alt+R",
          "keyChange": True,
          "multiple": True
          }


class Demo(QtGui.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()

        a2ctrl.check_ui_module(scope_widget_ui)

        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtGui.QFormLayout(w)
        w.setLayout(lyt)

        self.scope_widget = scope_widget.ScopeWidget(self)
        self.scope_widget.set_config(config)
        lyt.addRow('scope widget', self.scope_widget)

        a2ctrl.connect.cfg_controls(config, self.scope_widget.ui)
        self.scope_widget.changed.connect(self.bla)

        button = QtGui.QPushButton('set_config')
        button.clicked.connect(self.bla)
        lyt.addRow(button)

        # self.scope_widget.ui.cfg_scopeChange.clicked.connect(self.bla)
        # self.scope_widget.ui.cfg_scopeMode.currentIndexChanged.connect(self.bla)

    def bla(self):
        pprint(config)


def show():
    app = QtGui.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
