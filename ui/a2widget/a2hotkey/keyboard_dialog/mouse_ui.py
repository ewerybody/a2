# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mouse.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Mouse(object):
    def setupUi(self, Mouse):
        if not Mouse.objectName():
            Mouse.setObjectName(u"Mouse")
        Mouse.resize(420, 380)
        self.verticalLayout = QVBoxLayout(Mouse)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.inner_widget = QWidget(Mouse)
        self.inner_widget.setObjectName(u"inner_widget")
        self.inner_widget.setMaximumSize(QSize(420, 200))
        self.main_layout = QHBoxLayout(self.inner_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName(u"main_layout")
        self.lbutton = QPushButton(self.inner_widget)
        self.lbutton.setObjectName(u"lbutton")
        self.lbutton.setMinimumSize(QSize(0, 200))
        self.lbutton.setMaximumSize(QSize(100, 200))
        self.lbutton.setBaseSize(QSize(0, 0))

        self.main_layout.addWidget(self.lbutton)

        self.wheelleft = QPushButton(self.inner_widget)
        self.wheelleft.setObjectName(u"wheelleft")
        self.wheelleft.setMaximumSize(QSize(40, 180))

        self.main_layout.addWidget(self.wheelleft)

        self.middle_layout = QVBoxLayout()
        self.middle_layout.setSpacing(10)
        self.middle_layout.setObjectName(u"middle_layout")
        self.wheelup = QPushButton(self.inner_widget)
        self.wheelup.setObjectName(u"wheelup")
        self.wheelup.setMaximumSize(QSize(100, 40))

        self.middle_layout.addWidget(self.wheelup, 0, Qt.AlignTop)

        self.mbutton = QPushButton(self.inner_widget)
        self.mbutton.setObjectName(u"mbutton")
        self.mbutton.setMinimumSize(QSize(0, 100))
        self.mbutton.setMaximumSize(QSize(100, 16777215))

        self.middle_layout.addWidget(self.mbutton, 0, Qt.AlignVCenter)

        self.wheeldown = QPushButton(self.inner_widget)
        self.wheeldown.setObjectName(u"wheeldown")
        self.wheeldown.setMaximumSize(QSize(100, 40))

        self.middle_layout.addWidget(self.wheeldown, 0, Qt.AlignBottom)


        self.main_layout.addLayout(self.middle_layout)

        self.wheelright = QPushButton(self.inner_widget)
        self.wheelright.setObjectName(u"wheelright")
        self.wheelright.setMaximumSize(QSize(40, 180))

        self.main_layout.addWidget(self.wheelright)

        self.rbutton = QPushButton(self.inner_widget)
        self.rbutton.setObjectName(u"rbutton")
        self.rbutton.setMinimumSize(QSize(0, 200))
        self.rbutton.setMaximumSize(QSize(100, 200))

        self.main_layout.addWidget(self.rbutton)


        self.verticalLayout.addWidget(self.inner_widget)

        self._mouse_body = QPushButton(Mouse)
        self._mouse_body.setObjectName(u"_mouse_body")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._mouse_body.sizePolicy().hasHeightForWidth())
        self._mouse_body.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self._mouse_body)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Mouse)

        QMetaObject.connectSlotsByName(Mouse)
    # setupUi

    def retranslateUi(self, Mouse):
        Mouse.setWindowTitle(QCoreApplication.translate("Mouse", u"Form", None))
#if QT_CONFIG(tooltip)
        self.lbutton.setToolTip(QCoreApplication.translate("Mouse", u"Left Mouse Button", None))
#endif // QT_CONFIG(tooltip)
        self.lbutton.setText(QCoreApplication.translate("Mouse", u"L", None))
#if QT_CONFIG(tooltip)
        self.wheelleft.setToolTip(QCoreApplication.translate("Mouse", u"Wheel Left", None))
#endif // QT_CONFIG(tooltip)
        self.wheelleft.setText("")
#if QT_CONFIG(tooltip)
        self.wheelup.setToolTip(QCoreApplication.translate("Mouse", u"Wheel Up", None))
#endif // QT_CONFIG(tooltip)
        self.wheelup.setText("")
#if QT_CONFIG(tooltip)
        self.mbutton.setToolTip(QCoreApplication.translate("Mouse", u"Middle Mouse Button", None))
#endif // QT_CONFIG(tooltip)
        self.mbutton.setText(QCoreApplication.translate("Mouse", u"M", None))
#if QT_CONFIG(tooltip)
        self.wheeldown.setToolTip(QCoreApplication.translate("Mouse", u"Wheel Down", None))
#endif // QT_CONFIG(tooltip)
        self.wheeldown.setText("")
#if QT_CONFIG(tooltip)
        self.wheelright.setToolTip(QCoreApplication.translate("Mouse", u"Wheel Right", None))
#endif // QT_CONFIG(tooltip)
        self.wheelright.setText("")
#if QT_CONFIG(tooltip)
        self.rbutton.setToolTip(QCoreApplication.translate("Mouse", u"Right Mouse Button", None))
#endif // QT_CONFIG(tooltip)
        self.rbutton.setText(QCoreApplication.translate("Mouse", u"R", None))
        self._mouse_body.setText("")
    # retranslateUi

