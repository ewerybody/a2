# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\hotkey_func_widget.ui'
#
# Created: Wed May  2 15:32:05 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FuncWidget(object):
    def setupUi(self, FuncWidget):
        FuncWidget.setObjectName("FuncWidget")
        FuncWidget.resize(519, 56)
        self.verticalLayout = QtGui.QVBoxLayout(FuncWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.function_send_mode = QtGui.QComboBox(FuncWidget)
        self.function_send_mode.setObjectName("function_send_mode")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.function_send_mode.addItem("")
        self.horizontalLayout.addWidget(self.function_send_mode)
        self.run_label = QtGui.QLabel(FuncWidget)
        self.run_label.setObjectName("run_label")
        self.horizontalLayout.addWidget(self.run_label)
        self.functionText = QtGui.QLineEdit(FuncWidget)
        self.functionText.setObjectName("functionText")
        self.horizontalLayout.addWidget(self.functionText)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.functionRowLayout = QtGui.QHBoxLayout()
        self.functionRowLayout.setContentsMargins(-1, 0, -1, -1)
        self.functionRowLayout.setObjectName("functionRowLayout")
        self.cfg_functionMode = QtGui.QComboBox(FuncWidget)
        self.cfg_functionMode.setObjectName("cfg_functionMode")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.functionRowLayout.addWidget(self.cfg_functionMode)
        self.function_button = QtGui.QToolButton(FuncWidget)
        self.function_button.setText("...")
        self.function_button.setAutoRaise(True)
        self.function_button.setArrowType(QtCore.Qt.DownArrow)
        self.function_button.setObjectName("function_button")
        self.functionRowLayout.addWidget(self.function_button)
        self.functionButton = QtGui.QPushButton(FuncWidget)
        self.functionButton.setMaximumSize(QtCore.QSize(50, 35))
        self.functionButton.setObjectName("functionButton")
        self.functionRowLayout.addWidget(self.functionButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.functionRowLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.functionRowLayout)

        self.retranslateUi(FuncWidget)
        QtCore.QMetaObject.connectSlotsByName(FuncWidget)

    def retranslateUi(self, FuncWidget):
        FuncWidget.setWindowTitle(QtGui.QApplication.translate("FuncWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.function_send_mode.setItemText(0, QtGui.QApplication.translate("FuncWidget", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.function_send_mode.setItemText(1, QtGui.QApplication.translate("FuncWidget", "SendRaw", None, QtGui.QApplication.UnicodeUTF8))
        self.function_send_mode.setItemText(2, QtGui.QApplication.translate("FuncWidget", "SendInput", None, QtGui.QApplication.UnicodeUTF8))
        self.function_send_mode.setItemText(3, QtGui.QApplication.translate("FuncWidget", "SendPlay", None, QtGui.QApplication.UnicodeUTF8))
        self.function_send_mode.setItemText(4, QtGui.QApplication.translate("FuncWidget", "SendEvent", None, QtGui.QApplication.UnicodeUTF8))
        self.run_label.setText(QtGui.QApplication.translate("FuncWidget", "Run, ", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_functionMode.setItemText(0, QtGui.QApplication.translate("FuncWidget", "Run code", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_functionMode.setItemText(1, QtGui.QApplication.translate("FuncWidget", "Open file/url", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_functionMode.setItemText(2, QtGui.QApplication.translate("FuncWidget", "Send keystroke", None, QtGui.QApplication.UnicodeUTF8))
        self.functionButton.setText(QtGui.QApplication.translate("FuncWidget", "...", None, QtGui.QApplication.UnicodeUTF8))

