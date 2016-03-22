# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2ctrl\string_edit.ui'
#
# Created: Tue Mar 22 20:53:18 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_string_edit(object):
    def setupUi(self, string_edit):
        string_edit.setObjectName("string_edit")
        string_edit.resize(1138, 243)
        self.editLayout = QtGui.QVBoxLayout(string_edit)
        self.editLayout.setSpacing(5)
        self.editLayout.setContentsMargins(10, 5, 0, 5)
        self.editLayout.setObjectName("editLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(5)
        self.formLayout.setObjectName("formLayout")
        self.displayLabelLabel = QtGui.QLabel(string_edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtGui.QLineEdit(string_edit)
        self.cfg_label.setObjectName("cfg_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_label)
        self.displayLabelLabel_2 = QtGui.QLabel(string_edit)
        self.displayLabelLabel_2.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_2.setObjectName("displayLabelLabel_2")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.displayLabelLabel_2)
        self.cfg_value = QtGui.QLineEdit(string_edit)
        self.cfg_value.setText("")
        self.cfg_value.setObjectName("cfg_value")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.cfg_value)
        self.internalNameLabel = QtGui.QLabel(string_edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtGui.QLineEdit(string_edit)
        self.cfg_name.setObjectName("cfg_name")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cfg_name)
        self.editLayout.addLayout(self.formLayout)

        self.retranslateUi(string_edit)
        QtCore.QMetaObject.connectSlotsByName(string_edit)

    def retranslateUi(self, string_edit):
        string_edit.setWindowTitle(QtGui.QApplication.translate("string_edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("string_edit", "string label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("string_edit", "some string bla", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel_2.setText(QtGui.QApplication.translate("string_edit", "default text:", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("string_edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("string_edit", "extensionX_string1", None, QtGui.QApplication.UnicodeUTF8))

