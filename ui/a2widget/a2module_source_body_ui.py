# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2module_source_body.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QFormLayout, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from a2qt.QtCore import QMetaObject

from a2widget.a2path_field import A2PathField

class Ui_Form:
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName('Form')
        self.modsource_layout = QVBoxLayout(Form)
        self.modsource_layout.setObjectName('modsource_layout')
        self.frame = QFrame(Form)
        self.frame.setObjectName('frame')
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName('formLayout')
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName('label_2')
        self.label_2.setText('Maintainer:')
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName('label_3')
        self.label_3.setText('Homepage:')
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.homepage_label = QLabel(self.frame)
        self.homepage_label.setObjectName('homepage_label')
        self.homepage_label.setText('x')
        self.homepage_label.setOpenExternalLinks(True)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.homepage_label)
        self.description_label = QLabel(self.frame)
        self.description_label.setObjectName('description_label')
        self.description_label.setText('TextLabel')
        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.description_label)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName('label_4')
        self.label_4.setText('Version:')
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)
        self.maintainer_label = QLabel(self.frame)
        self.maintainer_label.setObjectName('maintainer_label')
        self.maintainer_label.setText('x')
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.maintainer_label)
        self.update_layout = QHBoxLayout()
        self.update_layout.setObjectName('update_layout')
        self.version_label = QLabel(self.frame)
        self.version_label.setObjectName('version_label')
        self.version_label.setText('x')
        self.update_layout.addWidget(self.version_label)
        self.update_button = QPushButton(self.frame)
        self.update_button.setObjectName('update_button')
        self.update_button.setText('check for updates ...')
        self.update_layout.addWidget(self.update_button)
        self.update_layout.setStretch(0, 1)
        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.update_layout)
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName('label_5')
        self.label_5.setText('Local Folder:')
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)
        self.local_path = A2PathField(self.frame)
        self.local_path.setObjectName('local_path')
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.local_path)
        self.modsource_layout.addWidget(self.frame)
        QMetaObject.connectSlotsByName(Form)
