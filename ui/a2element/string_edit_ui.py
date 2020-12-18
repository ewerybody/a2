# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'string_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from a2widget.a2text_field import A2TextField


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(495, 239)
        self.formLayout = QFormLayout(edit)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label = QLabel(edit)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.cfg_name = QLineEdit(edit)
        self.cfg_name.setObjectName(u"cfg_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cfg_name)

        self.label_2 = QLabel(edit)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cfg_label)

        self.cfg_label_over_field = QCheckBox(edit)
        self.cfg_label_over_field.setObjectName(u"cfg_label_over_field")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cfg_label_over_field)

        self.label_3 = QLabel(edit)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.cfg_value = A2TextField(edit)
        self.cfg_value.setObjectName(u"cfg_value")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cfg_value)

        self.cfg_password_mode = QCheckBox(edit)
        self.cfg_password_mode.setObjectName(u"cfg_password_mode")
        self.cfg_password_mode.setText(u"password mode (forces single line)")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.cfg_password_mode)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.label.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_string1", None))
        self.label_2.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"some string bla", None))
        self.cfg_label_over_field.setText(QCoreApplication.translate("edit", u"Label over field", None))
        self.label_3.setText(QCoreApplication.translate("edit", u"default text:", None))
    # retranslateUi

