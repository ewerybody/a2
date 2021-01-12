# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2module_source_body.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2path_field import A2PathField
from a2widget.a2more_button import A2MoreButton


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")

        self.modsource_layout = QVBoxLayout(Form)
        self.modsource_layout.setObjectName(u"modsource_layout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"Maintainer:")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setText(u"Homepage:")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.homepage_label = QLabel(self.frame)
        self.homepage_label.setObjectName(u"homepage_label")
        self.homepage_label.setText(u"x")
        self.homepage_label.setOpenExternalLinks(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.homepage_label)

        self.description_label = QLabel(self.frame)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setText(u"TextLabel")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.description_label)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setText(u"Version:")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.maintainer_label = QLabel(self.frame)
        self.maintainer_label.setObjectName(u"maintainer_label")
        self.maintainer_label.setText(u"x")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.maintainer_label)

        self.update_layout = QHBoxLayout()
        self.update_layout.setObjectName(u"update_layout")
        self.version_label = QLabel(self.frame)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setText(u"x")

        self.update_layout.addWidget(self.version_label)

        self.update_button = QPushButton(self.frame)
        self.update_button.setObjectName(u"update_button")
        self.update_button.setText(u"check for updates ...")

        self.update_layout.addWidget(self.update_button)

        self.a2option_button = A2MoreButton(self.frame)
        self.a2option_button.setObjectName(u"a2option_button")
        self.a2option_button.setText(u"")
        self.a2option_button.setAutoRaise(True)

        self.update_layout.addWidget(self.a2option_button)

        self.update_layout.setStretch(0, 1)

        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.update_layout)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setText(u"Local Folder:")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.local_path = A2PathField(self.frame)
        self.local_path.setObjectName(u"local_path")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.local_path)


        self.modsource_layout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        pass
    # retranslateUi

