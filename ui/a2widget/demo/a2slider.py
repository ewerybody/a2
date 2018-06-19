"""
a2widget.demo.a2slider

@created: 06.09.2016
@author: eric
"""
from a2widget import a2slider
from PySide2 import QtGui, QtCore, QtWidgets


class SliderDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(SliderDemo, self).__init__()
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        vlayout = QtWidgets.QVBoxLayout(widget)
        slider = a2slider.A2Slider(widget)
        slider.setMinimumWidth(500)

        slider.minmax = (0.001, 100.0)
        slider.value = 10
        slider.decimals = 3
        slider.step_len = 0.05

        slider.editing_finished.connect(self.finished)
        slider.value_changed.connect(self.changed)
        vlayout.addWidget(QtWidgets.QLabel('Slider with all connections and a field:'))
        vlayout.addWidget(slider)

        vlayout.addWidget(QtWidgets.QLabel('Slider without field and only finished connected but a custom label:'))
        hlayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('1.0')
        slider2 = a2slider.A2Slider(widget, has_field=False)
        hlayout.addWidget(self.label)
        hlayout.addWidget(slider2)
        slider2.editing_finished.connect(self.finished)
        slider2.value_changed.connect(self.label_update)
        vlayout.addLayout(hlayout)

        vlayout.addWidget(QtWidgets.QLabel('old slider'))
        old_slider = QtWidgets.QSlider(self)
        old_slider.setOrientation(QtCore.Qt.Horizontal)
        vlayout.addWidget(old_slider)
        old_slider.valueChanged.connect(self.changed)
        old_slider.sliderReleased.connect(self.finished)

    def label_update(self, value):
        self.label.setText(str(value))

    def finished(self, x=None):
        if x is None:
            print('    finished but nothing passed :(')
        else:
            print('    finished: %s' % x)

    def changed(self, x):
        print('    changed: %s' % x)


def show():
    app = QtWidgets.QApplication([])
    win = SliderDemo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
