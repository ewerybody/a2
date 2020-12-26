# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'button_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.local_script import ScriptSelector


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(607, 195)
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.displayLabelLabel)

        self.cfg_labeltext = QLineEdit(edit)
        self.cfg_labeltext.setObjectName(u"cfg_labeltext")
        self.cfg_labeltext.setText(u"")
        self.cfg_labeltext.setPlaceholderText(u"Space used by Button if empty!")

        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_labeltext)

        self.displayLabelLabel_2 = QLabel(edit)
        self.displayLabelLabel_2.setObjectName(u"displayLabelLabel_2")
        self.displayLabelLabel_2.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel_2)

        self.cfg_buttontext = QLineEdit(edit)
        self.cfg_buttontext.setObjectName(u"cfg_buttontext")

        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_buttontext)

        self.displayLabelLabel_3 = QLabel(edit)
        self.displayLabelLabel_3.setObjectName(u"displayLabelLabel_3")
        self.displayLabelLabel_3.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.displayLabelLabel_3)

        self.script_selector = ScriptSelector(edit)
        self.script_selector.setObjectName(u"script_selector")

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.script_selector)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"label text", None))
        self.displayLabelLabel_2.setText(QCoreApplication.translate("edit", u"button text", None))
        self.cfg_buttontext.setText("")
        self.cfg_buttontext.setPlaceholderText(QCoreApplication.translate("edit", u"Text to show on the Button.", None))
        self.displayLabelLabel_3.setText(QCoreApplication.translate("edit", u"python script", None))
    # retranslateUi

