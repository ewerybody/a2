from a2qt import QtCore, QtWidgets
from a2widget.flowlayout import FlowLayout
from a2widget.a2slider import A2Slider


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Flow Layout')

        main_layout = QtWidgets.QFormLayout(self)
        self.setLayout(main_layout)

        spacing = 5
        margin = 5

        flow = FlowLayout(margin=margin, spacing=spacing)
        flow.addWidget(QtWidgets.QPushButton('Short'))
        flow.addWidget(QtWidgets.QPushButton('Longer'))
        flow.addWidget(QtWidgets.QPushButton('Different text'))
        flow.addWidget(QtWidgets.QPushButton('More text'))
        flow.addWidget(QtWidgets.QPushButton('Even longer button text'))

        margin_slider = A2Slider(self, value=margin, mini=0, maxi=50, decimals=0)
        margin_slider.value_changed.connect(flow.set_marging)
        margin_slider.value_changed.connect(self._refresh_window)
        main_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('margin:'))
        main_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, margin_slider)

        spacing_slider = A2Slider(self, value=spacing, mini=0, maxi=50, decimals=0)
        spacing_slider.value_changed.connect(flow.set_spacing)
        spacing_slider.value_changed.connect(self._refresh_window)
        main_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel('spacing:'))
        main_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, spacing_slider)

        main_layout.setLayout(2, QtWidgets.QFormLayout.SpanningRole, flow)

    def _refresh_window(self, *_args):
        self.width()
        geo = self.geometry()
        sze = self.sizeHint()
        new_w = geo.width()
        new_h = geo.height()
        refresh = False
        if sze.width() > geo.width():
            new_w = sze.width()
            refresh = True
        if sze.height() > geo.height():
            new_h = sze.height()
            refresh = True
        if refresh:
            newgeo = QtCore.QRect(geo.x(), geo.y(), new_w, new_h)
            self.setGeometry(newgeo)


def show():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show()
