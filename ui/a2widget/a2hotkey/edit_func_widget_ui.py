# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\edit_func_widget.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\edit_func_widget.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_FuncWidget(object):
    def setupUi(self, FuncWidget):
        FuncWidget.setObjectName("FuncWidget")
        FuncWidget.resize(553, 83)
        self.verticalLayout = QtWidgets.QVBoxLayout(FuncWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.function_row_layout = QtWidgets.QHBoxLayout()
        self.function_row_layout.setContentsMargins(-1, 0, -1, -1)
        self.function_row_layout.setObjectName("function_row_layout")
        self.cfg_functionMode = QtWidgets.QComboBox(FuncWidget)
        self.cfg_functionMode.setObjectName("cfg_functionMode")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.function_row_layout.addWidget(self.cfg_functionMode)
        self.a2option_button = A2MoreButton(FuncWidget)
        self.a2option_button.setAutoRaise(True)
        self.a2option_button.setObjectName("a2option_button")
        self.function_row_layout.addWidget(self.a2option_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.function_row_layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.function_row_layout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.function_send_mode = QtWidgets.QComboBox(FuncWidget)
        self.function_send_mode.setObjectName("function_send_mode")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.horizontalLayout.addWidget(self.function_send_mode)
        self.run_label = QtWidgets.QLabel(FuncWidget)
        self.run_label.setObjectName("run_label")
        self.horizontalLayout.addWidget(self.run_label)
        self.function_text = QtWidgets.QLineEdit(FuncWidget)
        self.function_text.setObjectName("function_text")
        self.horizontalLayout.addWidget(self.function_text)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(FuncWidget)
        QtCore.QMetaObject.connectSlotsByName(FuncWidget)

    def retranslateUi(self, FuncWidget):
        FuncWidget.setWindowTitle(QtWidgets.QApplication.translate("FuncWidget", "Form", None, -1))
        self.cfg_functionMode.setItemText(0, QtWidgets.QApplication.translate("FuncWidget", "Run code", None, -1))
        self.cfg_functionMode.setItemText(1, QtWidgets.QApplication.translate("FuncWidget", "Open file/url", None, -1))
        self.cfg_functionMode.setItemText(2, QtWidgets.QApplication.translate("FuncWidget", "Send keystroke", None, -1))
        self.function_send_mode.setItemText(0, QtWidgets.QApplication.translate("FuncWidget", "Send", None, -1))
        self.function_send_mode.setItemText(1, QtWidgets.QApplication.translate("FuncWidget", "SendRaw", None, -1))
        self.function_send_mode.setItemText(2, QtWidgets.QApplication.translate("FuncWidget", "SendInput", None, -1))
        self.function_send_mode.setItemText(3, QtWidgets.QApplication.translate("FuncWidget", "SendPlay", None, -1))
        self.function_send_mode.setItemText(4, QtWidgets.QApplication.translate("FuncWidget", "SendEvent", None, -1))
        self.run_label.setText(QtWidgets.QApplication.translate("FuncWidget", "Run, ", None, -1))

from a2widget import A2MoreButton
