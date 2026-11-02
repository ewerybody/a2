"""
Form generated from reading UI file 'pathlist_edit.ui'

Created by: Qt User Interface Compiler version 6.12.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QSpinBox
from PySide6.QtCore import QMetaObject, QSize, Qt

from a2widget.a2text_field import A2InternalName


class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName('edit')
        edit.setWindowTitle('Form')
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName('edit_layout')
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName('internalNameLabel')
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setText('internal name:')
        self.internalNameLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.internalNameLabel)
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName('cfg_name')
        self.cfg_name.setText('extensionX_path1')
        self.edit_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfg_name)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName('displayLabelLabel')
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setText('display label:')
        self.displayLabelLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName('cfg_label')
        self.cfg_label.setText('some pathlist bla')
        self.edit_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfg_label)
        self.cfg_max_items = QSpinBox(edit)
        self.cfg_max_items.setObjectName('cfg_max_items')
        self.cfg_max_items.setSuffix('')
        self.cfg_max_items.setPrefix('')
        self.cfg_max_items.setMinimum(1)
        self.cfg_max_items.setMaximum(99)
        self.edit_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfg_max_items)
        self.maxItemsLabel = QLabel(edit)
        self.maxItemsLabel.setObjectName('maxItemsLabel')
        self.maxItemsLabel.setMinimumSize(QSize(100, 0))
        self.maxItemsLabel.setText('max items:')
        self.maxItemsLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.maxItemsLabel)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.cfg_browse_type_0 = QRadioButton(edit)
        self.cfg_browse_type_0.setObjectName('cfg_browse_type_0')
        self.cfg_browse_type_0.setText('folder')
        self.cfg_browse_type_0.setChecked(True)
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_0)
        self.cfg_browse_type_1 = QRadioButton(edit)
        self.cfg_browse_type_1.setObjectName('cfg_browse_type_1')
        self.cfg_browse_type_1.setText('file')
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.edit_layout.setLayout(3, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)
        self.label_3 = QLabel(edit)
        self.label_3.setObjectName('label_3')
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setText('type:')
        self.label_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_3)
        QMetaObject.connectSlotsByName(edit)
