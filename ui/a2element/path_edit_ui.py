# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'path_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from a2widget.a2path_field import A2PathField


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(488, 240)
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setContentsMargins(10, 5, 0, 5)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)

        self.cfg_name = QLineEdit(edit)
        self.cfg_name.setObjectName(u"cfg_name")

        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_name)

        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel)

        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")

        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_label)

        self.cfg_value = A2PathField(edit)
        self.cfg_value.setObjectName(u"cfg_value")

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_value)

        self.defaultPathLabel = QLabel(edit)
        self.defaultPathLabel.setObjectName(u"defaultPathLabel")
        self.defaultPathLabel.setMinimumSize(QSize(100, 0))
        self.defaultPathLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.defaultPathLabel)

        self.cfg_writable = QCheckBox(edit)
        self.cfg_writable.setObjectName(u"cfg_writable")

        self.edit_layout.setWidget(3, QFormLayout.FieldRole, self.cfg_writable)

        self.browse_type_layout = QHBoxLayout()
        self.browse_type_layout.setObjectName(u"browse_type_layout")
        self.cfg_browse_type_0 = QRadioButton(edit)
        self.cfg_browse_type_0.setObjectName(u"cfg_browse_type_0")

        self.browse_type_layout.addWidget(self.cfg_browse_type_0)

        self.cfg_browse_type_1 = QRadioButton(edit)
        self.cfg_browse_type_1.setObjectName(u"cfg_browse_type_1")
        self.cfg_browse_type_1.setChecked(True)

        self.browse_type_layout.addWidget(self.cfg_browse_type_1)

        self.cfg_save_mode = QCheckBox(edit)
        self.cfg_save_mode.setObjectName(u"cfg_save_mode")

        self.browse_type_layout.addWidget(self.cfg_save_mode)


        self.edit_layout.setLayout(4, QFormLayout.FieldRole, self.browse_type_layout)

        self.label_3 = QLabel(edit)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.file_types_label = QLabel(edit)
        self.file_types_label.setObjectName(u"file_types_label")
        self.file_types_label.setEnabled(True)
        self.file_types_label.setMinimumSize(QSize(100, 0))
        self.file_types_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(5, QFormLayout.LabelRole, self.file_types_label)

        self.cfg_file_types = QLineEdit(edit)
        self.cfg_file_types.setObjectName(u"cfg_file_types")

        self.edit_layout.setWidget(5, QFormLayout.FieldRole, self.cfg_file_types)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_path1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"some path bla", None))
        self.cfg_value.setText("")
        self.defaultPathLabel.setText(QCoreApplication.translate("edit", u"default path:", None))
        self.cfg_writable.setText(QCoreApplication.translate("edit", u"writable field", None))
        self.cfg_browse_type_0.setText(QCoreApplication.translate("edit", u"folder", None))
        self.cfg_browse_type_1.setText(QCoreApplication.translate("edit", u"file", None))
        self.cfg_save_mode.setText(QCoreApplication.translate("edit", u"save mode", None))
        self.label_3.setText(QCoreApplication.translate("edit", u"browse mode:", None))
        self.file_types_label.setText(QCoreApplication.translate("edit", u"file types:", None))
        self.cfg_file_types.setText("")
    # retranslateUi

