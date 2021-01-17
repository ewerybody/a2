# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nfo_edit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2tag_field import A2TagField


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")

        edit.setWindowTitle(u"Form")
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.cfg_description = QTextEdit(edit)
        self.cfg_description.setObjectName(u"cfg_description")
        self.cfg_description.setMaximumSize(QSize(16777215, 100))

        self.edit_layout.setWidget(0, QFormLayout.SpanningRole, self.cfg_description)

        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setText(u"Author:")
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.internalNameLabel)

        self.cfg_author = QLineEdit(edit)
        self.cfg_author.setObjectName(u"cfg_author")

        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_author)

        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setText(u"Version:")
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.displayLabelLabel)

        self.cfg_version = QLineEdit(edit)
        self.cfg_version.setObjectName(u"cfg_version")

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_version)

        self.label = QLabel(edit)
        self.label.setObjectName(u"label")
        self.label.setText(u"Date:")

        self.edit_layout.setWidget(3, QFormLayout.LabelRole, self.label)

        self.cfg_date = QLineEdit(edit)
        self.cfg_date.setObjectName(u"cfg_date")

        self.edit_layout.setWidget(3, QFormLayout.FieldRole, self.cfg_date)

        self.label_2 = QLabel(edit)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"URL:")

        self.edit_layout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.cfg_url = QLineEdit(edit)
        self.cfg_url.setObjectName(u"cfg_url")

        self.edit_layout.setWidget(4, QFormLayout.FieldRole, self.cfg_url)

        self.label_3 = QLabel(edit)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setText(u"Tags:")

        self.edit_layout.setWidget(5, QFormLayout.LabelRole, self.label_3)

        self.cfg_tags = A2TagField(edit)
        self.cfg_tags.setObjectName(u"cfg_tags")

        self.edit_layout.setWidget(5, QFormLayout.FieldRole, self.cfg_tags)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        pass
    # retranslateUi

