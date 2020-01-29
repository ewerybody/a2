# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2widget\a2input_dialog.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2widget\a2input_dialog.ui' applies.
#
# Created: Tue Jan 28 21:59:37 2020
#      by: pyside2-uic  running on PySide2 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_A2InputDialog(object):
    def setupUi(self, A2InputDialog):
        A2InputDialog.setObjectName("A2InputDialog")
        A2InputDialog.resize(368, 68)
        self.main_layout = QtWidgets.QVBoxLayout(A2InputDialog)
        self.main_layout.setObjectName("main_layout")
        self.label = QtWidgets.QLabel(A2InputDialog)
        self.label.setObjectName("label")
        self.main_layout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.a2ok_button = QtWidgets.QPushButton(A2InputDialog)
        self.a2ok_button.setObjectName("a2ok_button")
        self.horizontalLayout.addWidget(self.a2ok_button)
        self.a2cancel_button = QtWidgets.QPushButton(A2InputDialog)
        self.a2cancel_button.setFlat(True)
        self.a2cancel_button.setObjectName("a2cancel_button")
        self.horizontalLayout.addWidget(self.a2cancel_button)
        self.horizontalLayout.setStretch(0, 1)
        self.main_layout.addLayout(self.horizontalLayout)

        self.retranslateUi(A2InputDialog)
        QtCore.QMetaObject.connectSlotsByName(A2InputDialog)
        A2InputDialog.setTabOrder(self.a2ok_button, self.a2cancel_button)

    def retranslateUi(self, A2InputDialog):
        A2InputDialog.setWindowTitle(QtWidgets.QApplication.translate("A2InputDialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("A2InputDialog", "TextLabel", None, -1))
        self.a2ok_button.setText(QtWidgets.QApplication.translate("A2InputDialog", "OK", None, -1))
        self.a2cancel_button.setText(QtWidgets.QApplication.translate("A2InputDialog", "Cancel", None, -1))

