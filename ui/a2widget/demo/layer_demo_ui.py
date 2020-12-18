# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'layer_demo.ui'
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
        Form.resize(809, 441)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.layout_0 = QVBoxLayout()
        self.layout_0.setObjectName(u"layout_0")
        self.layout_0.setContentsMargins(-1, 0, -1, -1)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 635, 415))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout_0.addWidget(self.scrollArea)


        self.gridLayout.addLayout(self.layout_0, 0, 0, 1, 1)

        self.layout_1 = QVBoxLayout()
        self.layout_1.setObjectName(u"layout_1")
        self.layout_1.setContentsMargins(-1, -1, 40, 40)
        self.toolButton = QPushButton(Form)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMinimumSize(QSize(100, 50))
        self.toolButton.setMaximumSize(QSize(50, 50))

        self.layout_1.addWidget(self.toolButton, 0, Qt.AlignRight|Qt.AlignBottom)


        self.gridLayout.addLayout(self.layout_1, 0, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, Te"
                        "xtLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, TextLabel, ", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"Floater", None))
    # retranslateUi

