# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2licenses_widget.ui'
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
        Form.resize(677, 213)
        Form.setWindowTitle(u"")
        self.license_layout = QVBoxLayout(Form)
        self.license_layout.setObjectName(u"license_layout")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 631, 627))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.a2license_text = QLabel(self.scrollAreaWidgetContents)
        self.a2license_text.setObjectName(u"a2license_text")
        self.a2license_text.setText(u"<html><head/><body><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_ahk.png\"/><br/><span style=\" font-weight:600;\">AutoHotkey</span> - a scripting language for desktop automation - {ahk_version}</p><p align=\"center\"><a href=\"https://autohotkey.com\"><span style=\" text-decoration: underline; color:#0000ff;\">autohotkey.com</span></a> - <a href=\"https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU GPLv2</span></a></p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_python.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Python</span> - high-level programming language - {py_version}</p><p align=\"center\"><a href=\"https://www.python.org/\"><span style=\" text-decoration: underline; color:#0000ff;\">python.org</span></a> - <a href=\"https://docs.python.org/3/license.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Python Software Foundation License - GPL compatib"
                        "le</span></a></p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_pyside.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Qt for Python</span> - Python binding of the cross-platform GUI toolkit Qt - {qt_version}</p><p align=\"center\"><a href=\"https://www.qt.io/qt-for-python\"><span style=\" text-decoration: underline; color:#0000ff;\">qt.io/qt-for-python</span></a> - <a href=\"https://www.qt.io/licensing\"><span style=\" text-decoration: underline; color:#0000ff;\">LGPLv3/GPLv2</span></a></p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_material.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Material Icons</span> - Material Design icons by Google</p><p align=\"center\"><a href=\"https://material.io/icons\"><span style=\" text-decoration: underline; color:#0000ff;\">material.io/icons</span></a> - <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Apache License Ver"
                        "sion 2.0</span></a></p><p align=\"center\"><br/></p><p align=\"center\">Thanks so much!</p><p align=\"center\"><br/></p></body></html>")
        self.a2license_text.setWordWrap(True)
        self.a2license_text.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.a2license_text)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.license_layout.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        pass
    # retranslateUi

