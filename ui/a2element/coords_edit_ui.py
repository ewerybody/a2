# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'coords_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2coords_field import A2CoordsField


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(1010, 194)
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
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

        self.label = QLabel(edit)
        self.label.setObjectName(u"label")

        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.cfg_value = A2CoordsField(edit)
        self.cfg_value.setObjectName(u"cfg_value")

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_value)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_number1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"Some X/Y Coordinates", None))
        self.label.setText(QCoreApplication.translate("edit", u"default value:", None))
    # retranslateUi

