"""
a2widget.demo.a2slider

@created: 06.09.2016
@author: eric
Copyright 2001-2016 Crytek GmbH / Crytek Group. All rights reserved.
"""
from a2widget import a2slider
from PySide import QtGui


class SliderDemo(QtGui.QMainWindow):
    def __init__(self):
        super(SliderDemo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        w.setLayout(l)
        s = a2slider.A2Slider(w)
        s.setMinimumWidth(500)
        s.setSingleStep(0.1)
        s.setDecimals(2)
        s.setMinimum(0)
        s.setMaximum(2)
        s.editing_finished.connect(self.finished)
        s.value_changed.connect(self.changed)
        l.addWidget(QtGui.QLabel('Slider with all connections and a field:'))
        l.addWidget(s)

        l.addWidget(QtGui.QLabel('Slider without field and only finished connected but a custom label:'))
        h = QtGui.QHBoxLayout(w)
        self.label = QtGui.QLabel('1.0')
        s2 = a2slider.A2Slider(w, has_field=False)
        h.addWidget(self.label)
        h.addWidget(s2)
        s2.editing_finished.connect(self.finished)
        s2.value_changed.connect(self.label_update)
        l.addLayout(h)

    def label_update(self, value):
        self.label.setText(str(value))

    def finished(self, x):
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
