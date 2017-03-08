"""
a2widget.demo.a2slider

@created: 06.09.2016
@author: eric
Copyright 2001-2016 Crytek GmbH / Crytek Group. All rights reserved.
"""
from a2widget import a2slider
from PySide import QtGui, QtCore


class SliderDemo(QtGui.QMainWindow):
    def __init__(self):
        super(SliderDemo, self).__init__()
        w = QtGui.QWidget()
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        self.s = a2slider.A2Slider(w)
        self.s.setMinimumWidth(500)
        self.s.setSingleStep(0.1)
        self.s.setDecimals(2)
        self.s.setMinimum(0)
        self.s.setMaximum(2)
        self.s.editing_finished.connect(self.finished)
        self.s.value_changed.connect(self.changed)
        l.addWidget(QtGui.QLabel('Slider with all connections and a field:'))
        l.addWidget(self.s)

        l.addWidget(QtGui.QLabel('Slider without field and only finished connected but a custom label:'))
        h = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel('1.0')
        s2 = a2slider.A2Slider(w, has_field=False)
        h.addWidget(self.label)
        h.addWidget(s2)
        s2.editing_finished.connect(self.finished)
        s2.value_changed.connect(self.label_update)
        l.addLayout(h)

        l.addWidget(QtGui.QLabel('old slider'))
        o = QtGui.QSlider(self)
        o.setOrientation(QtCore.Qt.Horizontal)
        l.addWidget(o)
        o.valueChanged.connect(self.changed)
        o.sliderReleased.connect(self.finished)

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
    app = QtGui.QApplication([])
    win = SliderDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
