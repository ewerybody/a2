"""
For historic reasons ...
This was a super early layoyt draft for the a2 UI!

@author: eric
"""
import draft_ui
from PySide import QtGui


class Draft(QtGui.QMainWindow):
    def __init__(self):
        super(Draft, self).__init__()
        self.ui = draft_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.statusbar.showMessage('asdfas')


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = Draft()
    win.show()
    app.exec_()
