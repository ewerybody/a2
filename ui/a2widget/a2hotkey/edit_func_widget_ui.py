# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'edit_func_widget.ui'

Created by: Qt User Interface Compiler version 5.15.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2more_button import A2MoreButton


class Ui_FuncWidget:
    def setupUi(self, FuncWidget):
        if not FuncWidget.objectName():
            FuncWidget.setObjectName(u"FuncWidget")
        self.verticalLayout = QVBoxLayout(FuncWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.function_row_layout = QHBoxLayout()
        self.function_row_layout.setObjectName(u"function_row_layout")
        self.function_row_layout.setContentsMargins(-1, 0, -1, -1)
        self.cfg_functionMode = QComboBox(FuncWidget)
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.setObjectName(u"cfg_functionMode")
        self.function_row_layout.addWidget(self.cfg_functionMode)
        self.a2option_button = A2MoreButton(FuncWidget)
        self.a2option_button.setObjectName(u"a2option_button")
        self.a2option_button.setAutoRaise(True)
        self.function_row_layout.addWidget(self.a2option_button)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.function_row_layout.addItem(self.horizontalSpacer_3)
        self.verticalLayout.addLayout(self.function_row_layout)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.function_send_mode = QComboBox(FuncWidget)
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.setObjectName(u"function_send_mode")
        self.horizontalLayout.addWidget(self.function_send_mode)
        self.run_label = QLabel(FuncWidget)
        self.run_label.setObjectName(u"run_label")
        self.horizontalLayout.addWidget(self.run_label)
        self.function_text = QLineEdit(FuncWidget)
        self.function_text.setObjectName(u"function_text")
        self.horizontalLayout.addWidget(self.function_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(FuncWidget)
        QMetaObject.connectSlotsByName(FuncWidget)
    def retranslateUi(self, FuncWidget):
        FuncWidget.setWindowTitle(QCoreApplication.translate("FuncWidget", u"Form", None))
        self.cfg_functionMode.setItemText(0, QCoreApplication.translate("FuncWidget", u"Run code", None))
        self.cfg_functionMode.setItemText(1, QCoreApplication.translate("FuncWidget", u"Open file/url", None))
        self.cfg_functionMode.setItemText(2, QCoreApplication.translate("FuncWidget", u"Send keystroke", None))
        self.function_send_mode.setItemText(0, QCoreApplication.translate("FuncWidget", u"Send", None))
        self.function_send_mode.setItemText(1, QCoreApplication.translate("FuncWidget", u"SendRaw", None))
        self.function_send_mode.setItemText(2, QCoreApplication.translate("FuncWidget", u"SendInput", None))
        self.function_send_mode.setItemText(3, QCoreApplication.translate("FuncWidget", u"SendPlay", None))
        self.function_send_mode.setItemText(4, QCoreApplication.translate("FuncWidget", u"SendEvent", None))
        self.run_label.setText(QCoreApplication.translate("FuncWidget", u"Run, ", None))
