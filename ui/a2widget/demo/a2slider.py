"""
a2widget.demo.a2slider

@created: 06.09.2016
@author: eric
"""
from a2widget import a2slider
from PySide2 import QtCore, QtWidgets


class SliderDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(SliderDemo, self).__init__()
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        vlayout = QtWidgets.QVBoxLayout(widget)
        slider = a2slider.A2Slider(widget)
        slider.setMinimumWidth(500)

        slider.minmax = (0.001, 10.0)
        slider.value = 5
        slider.decimals = 3
        # slider.step_len = 10.0

        slider.editing_finished.connect(self.finished)
        slider.value_changed.connect(self.changed)
        vlayout.addWidget(QtWidgets.QLabel('Slider with all connections and a field:'))
        vlayout.addWidget(slider)

        vlayout.addWidget(QtWidgets.QLabel('Slider without field and only finished connected but a custom label:'))
        hlayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('1.0')
        self.label.setMinimumWidth(50)
        self.label.setMaximumWidth(50)
        slider2 = a2slider.A2Slider(widget, has_field=False)
        hlayout.addWidget(self.label)
        hlayout.addWidget(slider2)
        slider2.editing_finished.connect(self.finished)
        slider2.value_changed.connect(self.label_update)
        vlayout.addLayout(hlayout)

        log_slider = a2slider.A2Slider(widget)
        log_slider._log = True
        log_slider.minmax = (0.001, 25.0)
        log_slider.value = 1
        log_slider.decimals = 3
        log_slider.editing_finished.connect(self.finished)
        vlayout.addWidget(QtWidgets.QLabel('A logarithmic slider:'))
        vlayout.addWidget(log_slider)

        vlayout.addWidget(QtWidgets.QLabel('old slider'))
        old_slider = QtWidgets.QSlider(self)
        old_slider.setOrientation(QtCore.Qt.Horizontal)
        vlayout.addWidget(old_slider)
        old_slider.valueChanged.connect(self.changed)
        old_slider.sliderReleased.connect(self.finished)

    def label_update(self, value):
        self.label.setText(str(round(value, 2)))

    @staticmethod
    def finished(x=None):
        if x is None:
            print('    finished but nothing passed :(')
        else:
            print('    finished: %s' % x)

    @staticmethod
    def changed(x):
        print('    changed: %s' % x)


def show():
    app = QtWidgets.QApplication([])
    win = SliderDemo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
