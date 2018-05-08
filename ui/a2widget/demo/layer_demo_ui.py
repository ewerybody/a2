# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\demo\layer_demo.ui'
#
# Created: Tue May  8 16:30:45 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(652, 381)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.base_widget = QtGui.QWidget(Form)
        self.base_widget.setMinimumSize(QtCore.QSize(250, 250))
        self.base_widget.setObjectName("base_widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.base_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.base_widget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addWidget(self.base_widget, 0, 0, 1, 1)
        self.layout_1 = QtGui.QVBoxLayout()
        self.layout_1.setObjectName("layout_1")
        self.toolButton = QtGui.QToolButton(Form)
        self.toolButton.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton.setMaximumSize(QtCore.QSize(50, 50))
        self.toolButton.setText("")
        self.toolButton.setAutoRaise(True)
        self.toolButton.setArrowType(QtCore.Qt.DownArrow)
        self.toolButton.setObjectName("toolButton")
        self.layout_1.addWidget(self.toolButton)
        self.gridLayout.addLayout(self.layout_1, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, ", None, QtGui.QApplication.UnicodeUTF8))

