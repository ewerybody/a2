"""
Form generated from reading UI file 'coords_edit.ui'

Created by: Qt User Interface Compiler version 6.12.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import QFormLayout, QLabel, QLineEdit
from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt

from a2widget.a2coords_field import A2CoordsField
from a2widget.a2text_field import A2InternalName


class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName('edit')
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName('edit_layout')
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName('internalNameLabel')
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.internalNameLabel)
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName('cfg_name')
        self.edit_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfg_name)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName('displayLabelLabel')
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName('cfg_label')
        self.edit_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfg_label)
        self.label = QLabel(edit)
        self.label.setObjectName('label')
        self.edit_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)
        self.cfg_value = A2CoordsField(edit)
        self.cfg_value.setObjectName('cfg_value')
        self.edit_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfg_value)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate('edit', 'Form', None))
        self.internalNameLabel.setText(QCoreApplication.translate('edit', 'internal name:', None))
        self.cfg_name.setText(QCoreApplication.translate('edit', 'extensionX_number1', None))
        self.displayLabelLabel.setText(QCoreApplication.translate('edit', 'display label:', None))
        self.cfg_label.setText(QCoreApplication.translate('edit', 'Some X/Y Coordinates', None))
        self.label.setText(QCoreApplication.translate('edit', 'default value:', None))
