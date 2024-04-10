# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'edit_func_widget.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout
from a2qt.QtCore import QMetaObject

from a2widget.a2combo import A2Combo
from a2widget.a2more_button import A2MoreButton
from a2widget.a2path_field import A2PathField
from a2widget.a2text_field import A2CodeField

class Ui_FuncWidget:
    def setupUi(self, FuncWidget):
        if not FuncWidget.objectName():
            FuncWidget.setObjectName('FuncWidget')
        FuncWidget.setWindowTitle('Form')
        self.verticalLayout = QVBoxLayout(FuncWidget)
        self.verticalLayout.setObjectName('verticalLayout')
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.function_row_layout = QHBoxLayout()
        self.function_row_layout.setObjectName('function_row_layout')
        self.function_row_layout.setContentsMargins(-1, 0, -1, -1)
        self.cfg_functionMode = A2Combo(FuncWidget)
        self.cfg_functionMode.addItem(u"Run code")
        self.cfg_functionMode.addItem(u"Open file/url")
        self.cfg_functionMode.addItem(u"Send keystroke")
        self.cfg_functionMode.setObjectName('cfg_functionMode')
        self.function_row_layout.addWidget(self.cfg_functionMode)
        self.a2option_button = A2MoreButton(FuncWidget)
        self.a2option_button.setObjectName('a2option_button')
        self.a2option_button.setAutoRaise(True)
        self.function_row_layout.addWidget(self.a2option_button)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.function_row_layout.addItem(self.horizontalSpacer_3)
        self.verticalLayout.addLayout(self.function_row_layout)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.function_send_mode = A2Combo(FuncWidget)
        self.function_send_mode.addItem(u"Send")
        self.function_send_mode.addItem(u"SendRaw")
        self.function_send_mode.addItem(u"SendInput")
        self.function_send_mode.addItem(u"SendPlay")
        self.function_send_mode.addItem(u"SendEvent")
        self.function_send_mode.setObjectName('function_send_mode')
        self.horizontalLayout.addWidget(self.function_send_mode)
        self.run_label = QLabel(FuncWidget)
        self.run_label.setObjectName('run_label')
        self.run_label.setText('Run, ')
        self.horizontalLayout.addWidget(self.run_label)
        self.function_text = A2CodeField(FuncWidget)
        self.function_text.setObjectName('function_text')
        self.horizontalLayout.addWidget(self.function_text)
        self.run_url = A2PathField(FuncWidget)
        self.run_url.setObjectName('run_url')
        self.horizontalLayout.addWidget(self.run_url)
        self.verticalLayout.addLayout(self.horizontalLayout)
        QMetaObject.connectSlotsByName(FuncWidget)
