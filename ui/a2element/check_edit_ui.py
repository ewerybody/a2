# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'check_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(710, 146)
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
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

        self.cfg_value = QCheckBox(edit)
        self.cfg_value.setObjectName(u"cfg_value")
        self.cfg_value.setChecked(True)

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_value)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_checkbox1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"toggle some value On/Off", None))
        self.cfg_value.setText(QCoreApplication.translate("edit", u"enabled by default", None))
    # retranslateUi

