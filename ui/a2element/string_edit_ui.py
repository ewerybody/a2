"""
Form generated from reading UI file 'string_edit.ui'

Created by: Qt User Interface Compiler version 6.12.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import QCheckBox, QFormLayout, QLabel, QLineEdit
from PySide6.QtCore import QCoreApplication, QMetaObject, Qt

from a2widget.a2text_field import A2InternalName, A2TextField


class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName('edit')
        self.formLayout = QFormLayout(edit)
        self.formLayout.setObjectName('formLayout')
        self.formLayout.setLabelAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label = QLabel(edit)
        self.label.setObjectName('label')
        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName('cfg_name')
        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfg_name)
        self.label_2 = QLabel(edit)
        self.label_2.setObjectName('label_2')
        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName('cfg_label')
        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfg_label)
        self.cfg_label_over_field = QCheckBox(edit)
        self.cfg_label_over_field.setObjectName('cfg_label_over_field')
        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfg_label_over_field)
        self.label_3 = QLabel(edit)
        self.label_3.setObjectName('label_3')
        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_3)
        self.cfg_value = A2TextField(edit)
        self.cfg_value.setObjectName('cfg_value')
        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cfg_value)
        self.cfg_password_mode = QCheckBox(edit)
        self.cfg_password_mode.setObjectName('cfg_password_mode')
        self.cfg_password_mode.setText('password mode (forces single line)')
        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.cfg_password_mode)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate('edit', 'Form', None))
        self.label.setText(QCoreApplication.translate('edit', 'internal name:', None))
        self.cfg_name.setText(QCoreApplication.translate('edit', 'extensionX_string1', None))
        self.label_2.setText(QCoreApplication.translate('edit', 'display label:', None))
        self.cfg_label.setText(QCoreApplication.translate('edit', 'some string bla', None))
        self.cfg_label_over_field.setText(QCoreApplication.translate('edit', 'Label over field', None))
        self.label_3.setText(QCoreApplication.translate('edit', 'default text:', None))
