from a2qt import QtCore, QtWidgets
from a2widget import hover_widget


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        w.setMinimumSize(400, 200)
        self.setCentralWidget(w)
        lyt = QtWidgets.QFormLayout(w)
        self.setWindowTitle('HoverWidget Demo')

        text = 'Wrapped super long checkbox text text text text ... Wrapped super long checkbox text text text text ...'
        fancy_check1 = hover_widget.FancyCheck(text)
        fancy_check1.hover.mouse_pressed.connect(self.on_pressed)
        fancy_check1.hover.mouse_released.connect(self.on_released)
        lyt.addRow(fancy_check1)

        text = 'Rich text <b>on a Checkbox</b>!!<br>With linebreaks!🤯'
        fancy_check2 = hover_widget.FancyCheck(text)
        fancy_check2.hover.mouse_pressed.connect(self.on_pressed)
        fancy_check2.hover.mouse_released.connect(self.on_released)
        lyt.addRow(fancy_check2)

        self.label_pressed = QtWidgets.QLabel('Mouse Pressed')
        self.label_released = QtWidgets.QLabel('Mouse Released')
        hlyt = QtWidgets.QHBoxLayout()
        hlyt.addWidget(self.label_pressed)
        hlyt.addWidget(self.label_released)
        lyt.addRow(hlyt)
        self.label_pressed.hide()
        self.label_released.hide()

    def on_pressed(self):
        self.label_pressed.show()
        QtCore.QTimer(self).singleShot(500, self.label_pressed.hide)

    def on_released(self):
        self.label_released.show()
        QtCore.QTimer(self).singleShot(500, self.label_released.hide)


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
