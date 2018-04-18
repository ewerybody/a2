# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2input_dialog.ui'
#
# Created: Wed Apr 18 19:14:26 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_A2InputDialog(object):
    def setupUi(self, A2InputDialog):
        A2InputDialog.setObjectName("A2InputDialog")
        A2InputDialog.resize(368, 68)
        self.main_layout = QtGui.QVBoxLayout(A2InputDialog)
        self.main_layout.setObjectName("main_layout")
        self.label = QtGui.QLabel(A2InputDialog)
        self.label.setObjectName("label")
        self.main_layout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.a2ok_button = QtGui.QPushButton(A2InputDialog)
        self.a2ok_button.setObjectName("a2ok_button")
        self.horizontalLayout.addWidget(self.a2ok_button)
        self.a2cancel_button = QtGui.QPushButton(A2InputDialog)
        self.a2cancel_button.setFlat(True)
        self.a2cancel_button.setObjectName("a2cancel_button")
        self.horizontalLayout.addWidget(self.a2cancel_button)
        self.horizontalLayout.setStretch(0, 1)
        self.main_layout.addLayout(self.horizontalLayout)

        self.retranslateUi(A2InputDialog)
        QtCore.QMetaObject.connectSlotsByName(A2InputDialog)
        A2InputDialog.setTabOrder(self.a2ok_button, self.a2cancel_button)

    def retranslateUi(self, A2InputDialog):
        A2InputDialog.setWindowTitle(QtGui.QApplication.translate("A2InputDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("A2InputDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.a2ok_button.setText(QtGui.QApplication.translate("A2InputDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.a2cancel_button.setText(QtGui.QApplication.translate("A2InputDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

