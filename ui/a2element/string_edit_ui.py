# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\string_edit.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2element\string_edit.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(442, 105)
        self.edit_layout = QtWidgets.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setContentsMargins(10, 5, 0, 5)
        self.edit_layout.setObjectName("edit_layout")
        self.internalNameLabel = QtWidgets.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtWidgets.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QtWidgets.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtWidgets.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_label)
        self.displayLabelLabel_2 = QtWidgets.QLabel(edit)
        self.displayLabelLabel_2.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_2.setObjectName("displayLabelLabel_2")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel_2)
        self.cfg_value = QtWidgets.QLineEdit(edit)
        self.cfg_value.setText("")
        self.cfg_value.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.cfg_value.setObjectName("cfg_value")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_value)
        self.cfg_password_mode = QtWidgets.QCheckBox(edit)
        self.cfg_password_mode.setText("password mode")
        self.cfg_password_mode.setObjectName("cfg_password_mode")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_password_mode)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.internalNameLabel.setText(QtWidgets.QApplication.translate("edit", "internal name:", None, -1))
        self.cfg_name.setText(QtWidgets.QApplication.translate("edit", "extensionX_string1", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "display label:", None, -1))
        self.cfg_label.setText(QtWidgets.QApplication.translate("edit", "some string bla", None, -1))
        self.displayLabelLabel_2.setText(QtWidgets.QApplication.translate("edit", "default text:", None, -1))

