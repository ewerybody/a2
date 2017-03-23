from PySide import QtGui
from a2widget import A2TagField


class TagFieldDemo(QtGui.QMainWindow):
    def __init__(self):
        super(TagFieldDemo, self).__init__()
        self.setWindowTitle(self.__class__.__name__)
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QFormLayout(w)
        w.setLayout(l)

        self.c = A2TagField()
        self.c.available_tags = ['muppets', 'mopets', 'muffins']
        self.c.value = ['bla', 'lala']
        self.c.changed.connect(self.bla)

        l.setWidget(0, QtGui.QFormLayout.LabelRole, QtGui.QLabel('Tags:'))
        l.setWidget(0, QtGui.QFormLayout.FieldRole, self.c)

    def bla(self):
        print(self.c.value)
        #self.c.value = 'Blaab blaa!'


def show():
    app = QtGui.QApplication([])
    win = TagFieldDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
