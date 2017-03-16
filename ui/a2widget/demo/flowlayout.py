from PySide import QtCore, QtGui
from a2widget.flowlayout import FlowLayout


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        flowLayout = FlowLayout()
        flowLayout.addWidget(QtGui.QPushButton("Short"))
        flowLayout.addWidget(QtGui.QPushButton("Longer"))
        flowLayout.addWidget(QtGui.QPushButton("Different text"))
        flowLayout.addWidget(QtGui.QPushButton("More text"))
        flowLayout.addWidget(QtGui.QPushButton("Even longer button text"))
        self.setLayout(flowLayout)
        self.setWindowTitle("Flow Layout")


def show():
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show()
