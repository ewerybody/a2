# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2ctrl\string_edit.ui'
#
# Created: Wed Aug 31 22:44:11 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(508, 82)
        self.edit_layout = QtGui.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setContentsMargins(10, 5, 0, 5)
        self.edit_layout.setObjectName("edit_layout")
        self.internalNameLabel = QtGui.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtGui.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QtGui.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtGui.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cfg_label)
        self.displayLabelLabel_2 = QtGui.QLabel(edit)
        self.displayLabelLabel_2.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_2.setObjectName("displayLabelLabel_2")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.displayLabelLabel_2)
        self.cfg_value = QtGui.QLineEdit(edit)
        self.cfg_value.setText("")
        self.cfg_value.setObjectName("cfg_value")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_value)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("edit", "extensionX_string1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("edit", "some string bla", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel_2.setText(QtGui.QApplication.translate("edit", "default text:", None, QtGui.QApplication.UnicodeUTF8))

