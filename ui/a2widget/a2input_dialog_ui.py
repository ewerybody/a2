# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2input_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *


class Ui_A2InputDialog(object):
    def setupUi(self, A2InputDialog):
        if not A2InputDialog.objectName():
            A2InputDialog.setObjectName(u"A2InputDialog")

        self.main_layout = QVBoxLayout(A2InputDialog)
        self.main_layout.setObjectName(u"main_layout")
        self.label = QLabel(A2InputDialog)
        self.label.setObjectName(u"label")

        self.main_layout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.a2ok_button = QPushButton(A2InputDialog)
        self.a2ok_button.setObjectName(u"a2ok_button")

        self.horizontalLayout.addWidget(self.a2ok_button)

        self.a2cancel_button = QPushButton(A2InputDialog)
        self.a2cancel_button.setObjectName(u"a2cancel_button")
        self.a2cancel_button.setFlat(True)

        self.horizontalLayout.addWidget(self.a2cancel_button)

        self.horizontalLayout.setStretch(0, 1)

        self.main_layout.addLayout(self.horizontalLayout)

        QWidget.setTabOrder(self.a2ok_button, self.a2cancel_button)

        self.retranslateUi(A2InputDialog)

        QMetaObject.connectSlotsByName(A2InputDialog)
    # setupUi

    def retranslateUi(self, A2InputDialog):
        A2InputDialog.setWindowTitle(QCoreApplication.translate("A2InputDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("A2InputDialog", u"TextLabel", None))
        self.a2ok_button.setText(QCoreApplication.translate("A2InputDialog", u"OK", None))
        self.a2cancel_button.setText(QCoreApplication.translate("A2InputDialog", u"Cancel", None))
    # retranslateUi

