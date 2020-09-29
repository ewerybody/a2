from PySide2 import QtWidgets
from a2widget.a2tag_field import A2TagField


class TagFieldDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(TagFieldDemo, self).__init__()
        self.setWindowTitle(self.__class__.__name__)
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
        layout = QtWidgets.QFormLayout(widget)
        widget.setLayout(layout)

        self.tags = A2TagField()
        tags = ['muppets', 'mopets', 'muffins']
        self.tags.set_available_tags(tags)
        self.tags.value = ['bla', 'lala']
        self.tags.changed.connect(self.bla)

        layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('Tags:'))
        layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tags)

    def bla(self):
        print(self.tags.value)
        # self.tags.value = 'Blaab blaa!'


def show():
    app = QtWidgets.QApplication([])
    win = TagFieldDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
