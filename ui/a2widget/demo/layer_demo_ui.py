# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\demo\layer_demo.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\demo\layer_demo.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(652, 381)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.base_widget = QtWidgets.QWidget(Form)
        self.base_widget.setMinimumSize(QtCore.QSize(250, 250))
        self.base_widget.setObjectName("base_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.base_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.base_widget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addWidget(self.base_widget, 0, 0, 1, 1)
        self.layout_1 = QtWidgets.QVBoxLayout()
        self.layout_1.setObjectName("layout_1")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setMinimumSize(QtCore.QSize(50, 50))
        self.toolButton.setMaximumSize(QtCore.QSize(50, 50))
        self.toolButton.setText("")
        self.toolButton.setAutoRaise(True)
        self.toolButton.setArrowType(QtCore.Qt.DownArrow)
        self.toolButton.setObjectName("toolButton")
        self.layout_1.addWidget(self.toolButton)
        self.gridLayout.addLayout(self.layout_1, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, ", None, -1))

