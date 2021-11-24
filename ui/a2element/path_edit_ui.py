# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'path_edit.ui'

Created by: Qt User Interface Compiler version 6.2.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QCheckBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton
from a2qt.QtCore import QMetaObject, QSize, Qt

from a2widget.a2path_field import A2PathField
from a2widget.a2text_field import A2InternalName

class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.setWindowTitle(u"Form")
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setContentsMargins(10, 5, 0, 5)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setText(u"internal name:")
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName(u"cfg_name")
        self.cfg_name.setText(u"extensionX_path1")
        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setText(u"display label:")
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")
        self.cfg_label.setText(u"some path bla")
        self.cfg_label.setPlaceholderText(u"")
        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_label)
        self.cfg_value = A2PathField(edit)
        self.cfg_value.setObjectName(u"cfg_value")
        self.cfg_value.setText(u"")
        self.cfg_value.setPlaceholderText(u"")
        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_value)
        self.defaultPathLabel = QLabel(edit)
        self.defaultPathLabel.setObjectName(u"defaultPathLabel")
        self.defaultPathLabel.setMinimumSize(QSize(100, 0))
        self.defaultPathLabel.setText(u"default path:")
        self.defaultPathLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.defaultPathLabel)
        self.cfg_writable = QCheckBox(edit)
        self.cfg_writable.setObjectName(u"cfg_writable")
        self.cfg_writable.setText(u"writable field")
        self.edit_layout.setWidget(3, QFormLayout.FieldRole, self.cfg_writable)
        self.browse_type_layout = QHBoxLayout()
        self.browse_type_layout.setObjectName(u"browse_type_layout")
        self.cfg_browse_type_0 = QRadioButton(edit)
        self.cfg_browse_type_0.setObjectName(u"cfg_browse_type_0")
        self.cfg_browse_type_0.setText(u"folder")
        self.browse_type_layout.addWidget(self.cfg_browse_type_0)
        self.cfg_browse_type_1 = QRadioButton(edit)
        self.cfg_browse_type_1.setObjectName(u"cfg_browse_type_1")
        self.cfg_browse_type_1.setText(u"file")
        self.cfg_browse_type_1.setChecked(True)
        self.browse_type_layout.addWidget(self.cfg_browse_type_1)
        self.cfg_save_mode = QCheckBox(edit)
        self.cfg_save_mode.setObjectName(u"cfg_save_mode")
        self.cfg_save_mode.setText(u"save mode")
        self.browse_type_layout.addWidget(self.cfg_save_mode)
        self.edit_layout.setLayout(4, QFormLayout.FieldRole, self.browse_type_layout)
        self.label_3 = QLabel(edit)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setText(u"browse mode:")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(4, QFormLayout.LabelRole, self.label_3)
        self.file_types_label = QLabel(edit)
        self.file_types_label.setObjectName(u"file_types_label")
        self.file_types_label.setEnabled(True)
        self.file_types_label.setMinimumSize(QSize(100, 0))
        self.file_types_label.setText(u"file types:")
        self.file_types_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(5, QFormLayout.LabelRole, self.file_types_label)
        self.cfg_file_types = QLineEdit(edit)
        self.cfg_file_types.setObjectName(u"cfg_file_types")
        self.edit_layout.setWidget(5, QFormLayout.FieldRole, self.cfg_file_types)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)
    def retranslateUi(self, edit):
        self.cfg_file_types.setText("")
        pass
