# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2input_dialog.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from a2qt.QtCore import QCoreApplication, QMetaObject

class Ui_A2InputDialog:
    def setupUi(self, A2InputDialog):
        if not A2InputDialog.objectName():
            A2InputDialog.setObjectName('A2InputDialog')
        self.main_layout = QVBoxLayout(A2InputDialog)
        self.main_layout.setObjectName('main_layout')
        self.label = QLabel(A2InputDialog)
        self.label.setObjectName('label')
        self.label.setText('TextLabel')
        self.label.setOpenExternalLinks(True)
        self.main_layout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.a2ok_button = QPushButton(A2InputDialog)
        self.a2ok_button.setObjectName('a2ok_button')
        self.horizontalLayout.addWidget(self.a2ok_button)
        self.a2cancel_button = QPushButton(A2InputDialog)
        self.a2cancel_button.setObjectName('a2cancel_button')
        self.a2cancel_button.setFlat(True)
        self.horizontalLayout.addWidget(self.a2cancel_button)
        self.horizontalLayout.setStretch(0, 1)
        self.main_layout.addLayout(self.horizontalLayout)
        QWidget.setTabOrder(self.a2ok_button, self.a2cancel_button)
        self.retranslateUi(A2InputDialog)
        QMetaObject.connectSlotsByName(A2InputDialog)
    def retranslateUi(self, A2InputDialog):
        self.a2ok_button.setText(QCoreApplication.translate('A2InputDialog', 'OK', None))
        self.a2cancel_button.setText(QCoreApplication.translate('A2InputDialog', 'Cancel', None))
