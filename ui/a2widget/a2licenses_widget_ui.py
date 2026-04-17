# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2licenses_widget.ui'

Created by: Qt User Interface Compiler version 6.10.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from PySide6.QtCore import QMetaObject, QRect


class Ui_Form:
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName('Form')
        self.license_layout = QVBoxLayout(Form)
        self.license_layout.setObjectName('license_layout')
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 800, 755))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.a2license_text = QLabel(self.scrollAreaWidgetContents)
        self.a2license_text.setObjectName('a2license_text')
        self.a2license_text.setText(
            '<html><head/><body><p align="center"><br/></p><p align="center"><img src="../theme/logo_ahk.png"/><br/><span style=" font-weight:600;">AutoHotkey</span> - a scripting language for desktop automation - {ahk_version}</p><p align="center"><a href="https://autohotkey.com"><span style=" text-decoration: underline; color:#0000ff;">autohotkey.com</span></a> - <a href="https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"><span style=" text-decoration: underline; color:#0000ff;">GNU GPLv2</span></a></p><p align="center"><br/></p><p align="center"><img src="../theme/logo_python.png"/></p><p align="center"><span style=" font-weight:600;">Python</span> - high-level programming language - {py_version}</p><p align="center"><a href="https://www.python.org/"><span style=" text-decoration: underline; color:#0000ff;">python.org</span></a> - <a href="https://docs.python.org/3/license.html"><span style=" text-decoration: underline; color:#0000ff;">Python Software Foundation License - GP'
            'L compatible</span></a></p><p align="center"><br/></p><p align="center"><img src="../theme/logo_pyside.png"/></p><p align="center"><span style=" font-weight:600;">Qt for Python</span> - Python binding of the cross-platform GUI toolkit Qt - {qt_version}</p><p align="center"><a href="https://www.qt.io/qt-for-python"><span style=" text-decoration: underline; color:#0000ff;">qt.io/qt-for-python</span></a> - <a href="https://www.qt.io/licensing"><span style=" text-decoration: underline; color:#0000ff;">LGPLv3/GPLv2</span></a></p><p align="center"><br/></p><p align="center"><img src="../theme/logo_material.png"/></p><p align="center"><span style=" font-weight:600;">Material Icons</span> - Material Design icons by Google</p><p align="center"><a href="https://fonts.google.com/icons"><span style=" text-decoration: underline; color:#0000ff;">fonts.google.com/icons</span></a> - <a href="https://github.com/google/material-design-icons/blob/master/LICENSE"><span style=" text-decoratio'
            'n: underline; color:#0000ff;">Apache License Version 2.0</span></a></p><p align="center"><br/></p><p align="center">Thanks so much!</p><p align="center"><br/></p></body></html>'
        )
        self.a2license_text.setWordWrap(True)
        self.a2license_text.setOpenExternalLinks(True)
        self.verticalLayout_2.addWidget(self.a2license_text)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.license_layout.addWidget(self.scrollArea)
        QMetaObject.connectSlotsByName(Form)
