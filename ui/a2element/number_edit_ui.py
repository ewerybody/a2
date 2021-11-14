# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'number_edit.ui'

Created by: Qt User Interface Compiler version 5.15.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2text_field import A2InternalName


class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = A2InternalName(edit)
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
        self.value = QDoubleSpinBox(edit)
        self.value.setObjectName(u"value")
        self.value.setSuffix(u"")
        self.value.setDecimals(0)
        self.value.setSingleStep(1.000000000000000)
        self.value.setValue(0.000000000000000)
        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.value)
        self.label_2 = QLabel(edit)
        self.label_2.setObjectName(u"label_2")
        self.edit_layout.setWidget(3, QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.cfg_min = QDoubleSpinBox(edit)
        self.cfg_min.setObjectName(u"cfg_min")
        self.cfg_min.setMinimum(-16777215.000000000000000)
        self.cfg_min.setMaximum(16777215.000000000000000)
        self.cfg_min.setValue(0.000000000000000)
        self.horizontalLayout.addWidget(self.cfg_min)
        self.cfg_max = QDoubleSpinBox(edit)
        self.cfg_max.setObjectName(u"cfg_max")
        self.cfg_max.setMinimum(-16777215.000000000000000)
        self.cfg_max.setMaximum(16777215.000000000000000)
        self.cfg_max.setValue(100.000000000000000)
        self.horizontalLayout.addWidget(self.cfg_max)
        self.edit_layout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)
        self.label_3 = QLabel(edit)
        self.label_3.setObjectName(u"label_3")
        self.edit_layout.setWidget(4, QFormLayout.LabelRole, self.label_3)
        self.cfg_decimals = QSpinBox(edit)
        self.cfg_decimals.setObjectName(u"cfg_decimals")
        self.cfg_decimals.setValue(1)
        self.edit_layout.setWidget(4, QFormLayout.FieldRole, self.cfg_decimals)
        self.label_4 = QLabel(edit)
        self.label_4.setObjectName(u"label_4")
        self.edit_layout.setWidget(5, QFormLayout.LabelRole, self.label_4)
        self.cfg_step_len = QDoubleSpinBox(edit)
        self.cfg_step_len.setObjectName(u"cfg_step_len")
        self.cfg_step_len.setMaximum(16777215.000000000000000)
        self.cfg_step_len.setValue(1.000000000000000)
        self.edit_layout.setWidget(5, QFormLayout.FieldRole, self.cfg_step_len)
        self.label_5 = QLabel(edit)
        self.label_5.setObjectName(u"label_5")
        self.edit_layout.setWidget(6, QFormLayout.LabelRole, self.label_5)
        self.cfg_suffix = QLineEdit(edit)
        self.cfg_suffix.setObjectName(u"cfg_suffix")
        self.edit_layout.setWidget(6, QFormLayout.FieldRole, self.cfg_suffix)
        self.cfg_slider = QCheckBox(edit)
        self.cfg_slider.setObjectName(u"cfg_slider")
        self.edit_layout.setWidget(7, QFormLayout.FieldRole, self.cfg_slider)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)
    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_number1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"some number", None))
        self.label.setText(QCoreApplication.translate("edit", u"default value:", None))
        self.label_2.setText(QCoreApplication.translate("edit", u"min/max:", None))
        self.label_3.setText(QCoreApplication.translate("edit", u"decimals:", None))
        self.label_4.setText(QCoreApplication.translate("edit", u"step length:", None))
        self.label_5.setText(QCoreApplication.translate("edit", u"suffix label:", None))
        self.cfg_slider.setText(QCoreApplication.translate("edit", u"show slider", None))
