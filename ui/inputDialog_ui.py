# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\inputDialog.ui'
#
# Created: Sun Sep 20 22:20:37 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_InputDialog(object):
    def setupUi(self, InputDialog):
        InputDialog.setObjectName("InputDialog")
        InputDialog.resize(800, 168)
        self.verticalLayout = QtGui.QVBoxLayout(InputDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(InputDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textField = QtGui.QLineEdit(InputDialog)
        self.textField.setObjectName("textField")
        self.verticalLayout.addWidget(self.textField)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.okButton = QtGui.QPushButton(InputDialog)
        self.okButton.setStyleSheet("* {background-color: #43B6FF;}")
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(InputDialog)
        self.cancelButton.setFlat(True)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(InputDialog)
        QtCore.QMetaObject.connectSlotsByName(InputDialog)
        InputDialog.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, InputDialog):
        InputDialog.setWindowTitle(QtGui.QApplication.translate("InputDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("InputDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("InputDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("InputDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

