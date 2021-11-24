# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'check_edit.ui'

Created by: Qt User Interface Compiler version 6.2.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QCheckBox, QFormLayout, QLabel, QLineEdit
from a2qt.QtCore import QMetaObject, QSize, Qt

from a2widget.a2text_field import A2InternalName

class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.setWindowTitle(u"Form")
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName(u"cfg_name")
        self.cfg_name.setText(u"extensionX_checkbox1")
        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_name)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setText(u"internal name:")
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setText(u"display label:")
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")
        self.cfg_label.setText(u"toggle some value On/Off")
        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_label)
        self.cfg_value = QCheckBox(edit)
        self.cfg_value.setObjectName(u"cfg_value")
        self.cfg_value.setText(u"enabled by default")
        self.cfg_value.setChecked(True)
        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_value)
        QMetaObject.connectSlotsByName(edit)
