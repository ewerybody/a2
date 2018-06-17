# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\group_edit.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2element\group_edit.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(822, 130)
        self.edit_layout = QtWidgets.QVBoxLayout(edit)
        self.edit_layout.setContentsMargins(-1, -1, 0, -1)
        self.edit_layout.setObjectName("edit_layout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setSpacing(5)
        self.formLayout.setObjectName("formLayout")
        self.internalNameLabel = QtWidgets.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtWidgets.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QtWidgets.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtWidgets.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_label)
        self.cfg_disablable = QtWidgets.QCheckBox(edit)
        self.cfg_disablable.setChecked(True)
        self.cfg_disablable.setObjectName("cfg_disablable")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_disablable)
        self.cfg_enabled = QtWidgets.QCheckBox(edit)
        self.cfg_enabled.setChecked(True)
        self.cfg_enabled.setObjectName("cfg_enabled")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_enabled)
        self.edit_layout.addLayout(self.formLayout)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.internalNameLabel.setText(QtWidgets.QApplication.translate("edit", "internal name:", None, -1))
        self.cfg_name.setText(QtWidgets.QApplication.translate("edit", "extensionX_group1", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "display label:", None, -1))
        self.cfg_label.setText(QtWidgets.QApplication.translate("edit", "some group name", None, -1))
        self.cfg_disablable.setText(QtWidgets.QApplication.translate("edit", "checkable", None, -1))
        self.cfg_enabled.setText(QtWidgets.QApplication.translate("edit", "enabled by default", None, -1))

