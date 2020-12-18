# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2module_source.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(778, 67)
        self.modsource_layout = QVBoxLayout(Form)
        self.modsource_layout.setObjectName(u"modsource_layout")
        self.modsource_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout = QHBoxLayout()
        self.header_layout.setObjectName(u"header_layout")
        self.check = QCheckBox(Form)
        self.check.setObjectName(u"check")
        self.check.setText(u"")

        self.header_layout.addWidget(self.check)

        self.tool_button = QToolButton(Form)
        self.tool_button.setObjectName(u"tool_button")
        self.tool_button.setText(u"...")
        self.tool_button.setAutoRaise(True)
        self.tool_button.setArrowType(Qt.RightArrow)

        self.header_layout.addWidget(self.tool_button)

        self.label_widget = QWidget(Form)
        self.label_widget.setObjectName(u"label_widget")
        self.labels_layout = QHBoxLayout(self.label_widget)
        self.labels_layout.setObjectName(u"labels_layout")
        self.labels_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_label = QLabel(self.label_widget)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setMinimumSize(QSize(20, 20))
        self.icon_label.setText(u"")

        self.labels_layout.addWidget(self.icon_label)

        self.mod_label = QLabel(self.label_widget)
        self.mod_label.setObjectName(u"mod_label")
        self.mod_label.setMinimumSize(QSize(40, 0))
        font = QFont()
        font.setBold(True)
        self.mod_label.setFont(font)
        self.mod_label.setText(u"ModSourceName")

        self.labels_layout.addWidget(self.mod_label)

        self.extra_label = QLabel(self.label_widget)
        self.extra_label.setObjectName(u"extra_label")
        self.extra_label.setMinimumSize(QSize(40, 0))
        self.extra_label.setText(u"(extra)")

        self.labels_layout.addWidget(self.extra_label)

        self.mod_count = QLabel(self.label_widget)
        self.mod_count.setObjectName(u"mod_count")
        self.mod_count.setText(u"TextLabel")
        self.mod_count.setAlignment(Qt.AlignCenter)

        self.labels_layout.addWidget(self.mod_count)

        self.labels_layout.setStretch(3, 1)

        self.header_layout.addWidget(self.label_widget)

        self.error_icon = QToolButton(Form)
        self.error_icon.setObjectName(u"error_icon")
        self.error_icon.setEnabled(False)
        self.error_icon.setText(u"...")
        self.error_icon.setAutoRaise(True)
        self.error_icon.setArrowType(Qt.NoArrow)

        self.header_layout.addWidget(self.error_icon)

        self.header_layout.setStretch(2, 1)

        self.modsource_layout.addLayout(self.header_layout)

        self.details_widget = QWidget(Form)
        self.details_widget.setObjectName(u"details_widget")

        self.modsource_layout.addWidget(self.details_widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        pass
    # retranslateUi

