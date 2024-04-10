# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'menu_item_edit.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QFormLayout, QLabel, QLineEdit
from a2qt.QtCore import QCoreApplication, QMetaObject, QSize, Qt

from a2widget.local_script import ScriptSelector

class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName('edit')
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName('edit_layout')
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName('displayLabelLabel')
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName('cfg_label')
        self.cfg_label.setText('')
        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_label)
        self.displayLabelLabel_3 = QLabel(edit)
        self.displayLabelLabel_3.setObjectName('displayLabelLabel_3')
        self.displayLabelLabel_3.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel_3)
        self.script_selector = ScriptSelector(edit)
        self.script_selector.setObjectName('script_selector')
        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.script_selector)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)
    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate('edit', 'Form', None))
        self.displayLabelLabel.setText(QCoreApplication.translate('edit', 'display label', None))
        self.displayLabelLabel_3.setText(QCoreApplication.translate('edit', 'python script', None))
