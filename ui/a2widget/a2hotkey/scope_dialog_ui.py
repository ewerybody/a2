# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\scope_dialog.ui'
#
# Created: Thu May  3 17:53:49 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ScopeDialog(object):
    def setupUi(self, ScopeDialog):
        ScopeDialog.setObjectName("ScopeDialog")
        ScopeDialog.resize(413, 152)
        self.formLayout = QtGui.QFormLayout(ScopeDialog)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(ScopeDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.scope_title = A2ButtonField(ScopeDialog)
        self.scope_title.setObjectName("scope_title")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.scope_title)
        self.label_3 = QtGui.QLabel(ScopeDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.scope_class = A2ButtonField(ScopeDialog)
        self.scope_class.setObjectName("scope_class")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.scope_class)
        self.label_4 = QtGui.QLabel(ScopeDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.scope_exe = A2ButtonField(ScopeDialog)
        self.scope_exe.setObjectName("scope_exe")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.scope_exe)
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
        self.formLayout.setLayout(4, QtGui.QFormLayout.SpanningRole, self.horizontalLayout)
        self.scope_string = A2ButtonField(ScopeDialog)
        self.scope_string.setToolTip("")
        self.scope_string.setReadOnly(True)
        self.scope_string.setObjectName("scope_string")
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.scope_string)

        self.retranslateUi(ScopeDialog)
        QtCore.QMetaObject.connectSlotsByName(ScopeDialog)
        ScopeDialog.setTabOrder(self.a2ok_button, self.a2cancel_button)

    def retranslateUi(self, ScopeDialog):
        ScopeDialog.setWindowTitle(QtGui.QApplication.translate("ScopeDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ScopeDialog", "title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ScopeDialog", "window class", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ScopeDialog", "executable", None, QtGui.QApplication.UnicodeUTF8))
        self.a2ok_button.setText(QtGui.QApplication.translate("ScopeDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.a2cancel_button.setText(QtGui.QApplication.translate("ScopeDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from a2widget.a2button_field import A2ButtonField
