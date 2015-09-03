# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\scopeDialog.ui'
#
# Created: Thu Sep  3 09:49:58 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ScopeDialog(object):
    def setupUi(self, ScopeDialog):
        ScopeDialog.setObjectName("ScopeDialog")
        ScopeDialog.resize(1091, 285)
        self.verticalLayout = QtGui.QVBoxLayout(ScopeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.scopeText = QtGui.QLineEdit(ScopeDialog)
        self.scopeText.setReadOnly(True)
        self.scopeText.setObjectName("scopeText")
        self.horizontalLayout_5.addWidget(self.scopeText)
        self.helpButton = QtGui.QPushButton(ScopeDialog)
        self.helpButton.setObjectName("helpButton")
        self.horizontalLayout_5.addWidget(self.helpButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(ScopeDialog)
        self.label_2.setMinimumSize(QtCore.QSize(200, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.scopeTitle = QtGui.QLineEdit(ScopeDialog)
        self.scopeTitle.setObjectName("scopeTitle")
        self.horizontalLayout_2.addWidget(self.scopeTitle)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(ScopeDialog)
        self.label_3.setMinimumSize(QtCore.QSize(200, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.scopeClass = QtGui.QLineEdit(ScopeDialog)
        self.scopeClass.setObjectName("scopeClass")
        self.horizontalLayout_3.addWidget(self.scopeClass)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtGui.QLabel(ScopeDialog)
        self.label_4.setMinimumSize(QtCore.QSize(200, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.scopeExe = QtGui.QLineEdit(ScopeDialog)
        self.scopeExe.setObjectName("scopeExe")
        self.horizontalLayout_4.addWidget(self.scopeExe)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.okButton = QtGui.QPushButton(ScopeDialog)
        self.okButton.setStyleSheet("* {background-color: #43B6FF;}")
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(ScopeDialog)
        self.cancelButton.setFlat(True)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ScopeDialog)
        QtCore.QMetaObject.connectSlotsByName(ScopeDialog)

    def retranslateUi(self, ScopeDialog):
        ScopeDialog.setWindowTitle(QtGui.QApplication.translate("ScopeDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("ScopeDialog", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ScopeDialog", "title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ScopeDialog", "window class", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ScopeDialog", "executable", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("ScopeDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("ScopeDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

