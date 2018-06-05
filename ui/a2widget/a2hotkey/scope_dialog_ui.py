# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\scope_dialog.ui'
#
# Created: Fri Jun  1 15:32:50 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ScopeDialog(object):
    def setupUi(self, ScopeDialog):
        ScopeDialog.setObjectName("ScopeDialog")
        ScopeDialog.resize(1063, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ScopeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.display_only_label = QtGui.QLabel(ScopeDialog)
        self.display_only_label.setObjectName("display_only_label")
        self.verticalLayout.addWidget(self.display_only_label)
        self.scope_widget = ScopeWidget(ScopeDialog)
        self.scope_widget.setObjectName("scope_widget")
        self.verticalLayout.addWidget(self.scope_widget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.a2ok_button = QtGui.QPushButton(ScopeDialog)
        self.a2ok_button.setObjectName("a2ok_button")
        self.horizontalLayout.addWidget(self.a2ok_button)
        self.a2cancel_button = QtGui.QPushButton(ScopeDialog)
        self.a2cancel_button.setFlat(True)
        self.a2cancel_button.setObjectName("a2cancel_button")
        self.horizontalLayout.addWidget(self.a2cancel_button)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ScopeDialog)
        QtCore.QObject.connect(self.a2ok_button, QtCore.SIGNAL("clicked()"), ScopeDialog.accept)
        QtCore.QObject.connect(self.a2cancel_button, QtCore.SIGNAL("clicked()"), ScopeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ScopeDialog)
        ScopeDialog.setTabOrder(self.a2ok_button, self.a2cancel_button)

    def retranslateUi(self, ScopeDialog):
        ScopeDialog.setWindowTitle(QtGui.QApplication.translate("ScopeDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.display_only_label.setText(QtGui.QApplication.translate("ScopeDialog", "This is for display only! The scope cannot be changed.", None, QtGui.QApplication.UnicodeUTF8))
        self.a2ok_button.setText(QtGui.QApplication.translate("ScopeDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.a2cancel_button.setText(QtGui.QApplication.translate("ScopeDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from a2widget.a2hotkey.scope_widget import ScopeWidget
