# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\keyboard_dialog\mouse.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\keyboard_dialog\mouse.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_Mouse(object):
    def setupUi(self, Mouse):
        Mouse.setObjectName("Mouse")
        Mouse.resize(420, 380)
        self.verticalLayout = QtWidgets.QVBoxLayout(Mouse)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inner_widget = QtWidgets.QWidget(Mouse)
        self.inner_widget.setMaximumSize(QtCore.QSize(420, 200))
        self.inner_widget.setObjectName("inner_widget")
        self.main_layout = QtWidgets.QHBoxLayout(self.inner_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        self.lbutton = QtWidgets.QPushButton(self.inner_widget)
        self.lbutton.setMinimumSize(QtCore.QSize(0, 200))
        self.lbutton.setMaximumSize(QtCore.QSize(100, 200))
        self.lbutton.setBaseSize(QtCore.QSize(0, 0))
        self.lbutton.setObjectName("lbutton")
        self.main_layout.addWidget(self.lbutton)
        self.wheelleft = QtWidgets.QPushButton(self.inner_widget)
        self.wheelleft.setMaximumSize(QtCore.QSize(40, 180))
        self.wheelleft.setText("")
        self.wheelleft.setObjectName("wheelleft")
        self.main_layout.addWidget(self.wheelleft)
        self.middle_layout = QtWidgets.QVBoxLayout()
        self.middle_layout.setSpacing(10)
        self.middle_layout.setObjectName("middle_layout")
        self.wheelup = QtWidgets.QPushButton(self.inner_widget)
        self.wheelup.setMaximumSize(QtCore.QSize(100, 40))
        self.wheelup.setText("")
        self.wheelup.setObjectName("wheelup")
        self.middle_layout.addWidget(self.wheelup)
        self.mbutton = QtWidgets.QPushButton(self.inner_widget)
        self.mbutton.setMinimumSize(QtCore.QSize(0, 100))
        self.mbutton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.mbutton.setObjectName("mbutton")
        self.middle_layout.addWidget(self.mbutton)
        self.wheeldown = QtWidgets.QPushButton(self.inner_widget)
        self.wheeldown.setMaximumSize(QtCore.QSize(100, 40))
        self.wheeldown.setText("")
        self.wheeldown.setObjectName("wheeldown")
        self.middle_layout.addWidget(self.wheeldown)
        self.main_layout.addLayout(self.middle_layout)
        self.wheelright = QtWidgets.QPushButton(self.inner_widget)
        self.wheelright.setMaximumSize(QtCore.QSize(40, 180))
        self.wheelright.setText("")
        self.wheelright.setObjectName("wheelright")
        self.main_layout.addWidget(self.wheelright)
        self.rbutton = QtWidgets.QPushButton(self.inner_widget)
        self.rbutton.setMinimumSize(QtCore.QSize(0, 200))
        self.rbutton.setMaximumSize(QtCore.QSize(100, 200))
        self.rbutton.setObjectName("rbutton")
        self.main_layout.addWidget(self.rbutton)
        self.verticalLayout.addWidget(self.inner_widget)
        self._mouse_body = QtWidgets.QPushButton(Mouse)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._mouse_body.sizePolicy().hasHeightForWidth())
        self._mouse_body.setSizePolicy(sizePolicy)
        self._mouse_body.setText("")
        self._mouse_body.setObjectName("_mouse_body")
        self.verticalLayout.addWidget(self._mouse_body)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Mouse)
        QtCore.QMetaObject.connectSlotsByName(Mouse)

    def retranslateUi(self, Mouse):
        Mouse.setWindowTitle(QtWidgets.QApplication.translate("Mouse", "Form", None, -1))
        self.lbutton.setToolTip(QtWidgets.QApplication.translate("Mouse", "Left Mouse Button", None, -1))
        self.lbutton.setText(QtWidgets.QApplication.translate("Mouse", "L", None, -1))
        self.wheelleft.setToolTip(QtWidgets.QApplication.translate("Mouse", "Wheel Left", None, -1))
        self.wheelup.setToolTip(QtWidgets.QApplication.translate("Mouse", "Wheel Up", None, -1))
        self.mbutton.setToolTip(QtWidgets.QApplication.translate("Mouse", "Middle Mouse Button", None, -1))
        self.mbutton.setText(QtWidgets.QApplication.translate("Mouse", "M", None, -1))
        self.wheeldown.setToolTip(QtWidgets.QApplication.translate("Mouse", "Wheel Down", None, -1))
        self.wheelright.setToolTip(QtWidgets.QApplication.translate("Mouse", "Wheel Right", None, -1))
        self.rbutton.setToolTip(QtWidgets.QApplication.translate("Mouse", "Right Mouse Button", None, -1))
        self.rbutton.setText(QtWidgets.QApplication.translate("Mouse", "R", None, -1))

