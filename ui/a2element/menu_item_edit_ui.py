# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu_item_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from a2widget.local_script import ScriptSelector


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(549, 86)
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.displayLabelLabel)

        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")
        self.cfg_label.setText(u"")

        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_label)

        self.displayLabelLabel_3 = QLabel(edit)
        self.displayLabelLabel_3.setObjectName(u"displayLabelLabel_3")
        self.displayLabelLabel_3.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel_3)

        self.script_selector = ScriptSelector(edit)
        self.script_selector.setObjectName(u"script_selector")

        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.script_selector)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label", None))
        self.displayLabelLabel_3.setText(QCoreApplication.translate("edit", u"python script", None))
    # retranslateUi

