from PySide2 import QtWidgets
from a2widget.a2tag_field import A2TagField


class TagFieldDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(TagFieldDemo, self).__init__()
        self.setWindowTitle(self.__class__.__name__)
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        l = QtWidgets.QFormLayout(w)
        w.setLayout(l)

        self.c = A2TagField()
        tags = ['muppets', 'mopets', 'muffins']
        self.c.set_available_tags(tags)
        self.c.value = ['bla', 'lala']
        self.c.changed.connect(self.bla)

        l.setWidget(0, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('Tags:'))
        l.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.c)

    def bla(self):
        print(self.c.value)
        # self.c.value = 'Blaab blaa!'


def show():
    app = QtWidgets.QApplication([])
    win = TagFieldDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
