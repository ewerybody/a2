# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file:
#   'c:\Users\eric\io\code\a2\ui\a2widget\a2licenses_widget.ui'
# licensing of that file applies.
#
# Created: Sat Jun 27 16:18:41 2020
#      by: pyside2-uic  running on PySide2 5.15.0
#
# pylint: disable=W0201,C0103,C0111
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(676, 584)
        Form.setWindowTitle("")
        self.license_layout = QtWidgets.QVBoxLayout(Form)
        self.license_layout.setObjectName("license_layout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 630, 649))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.a2license_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.a2license_text.setText("<html><head/><body><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_ahk.png\"/><br/><span style=\" font-weight:600;\">AutoHotkey</span> - a scripting language for desktop automation - {ahk_version}</p><p align=\"center\"><a href=\"https://autohotkey.com\"><span style=\" text-decoration: underline; color:#0000ff;\">autohotkey.com</span></a> - <a href=\"https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU GPLv2</span></a></p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_python.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Python</span> - high-level programming language - {py_version}</p><p align=\"center\"><a href=\"https://www.python.org/\"><span style=\" text-decoration: underline; color:#0000ff;\">python.org</span></a> - <a href=\"https://docs.python.org/3/license.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Python Software Foundation License - GPL compatible</span></a></p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_pyside.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Qt for Python</span> - Python binding of the cross-platform GUI toolkit Qt - {qt_version}</p><p align=\"center\"><a href=\"https://www.qt.io/qt-for-python\"><span style=\" text-decoration: underline; color:#0000ff;\">qt.io/qt-for-python</span></a> - <a href=\"https://www.qt.io/licensing\"><span style=\" text-decoration: underline; color:#0000ff;\">LGPLv3/GPLv2</span></a></p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_material.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Material Icons</span> - Material Design icons by Google</p><p align=\"center\"><a href=\"https://material.io/icons\"><span style=\" text-decoration: underline; color:#0000ff;\">material.io/icons</span></a> - <a href=\"https://www.apache.org/licenses/LICENSE-2.0.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Apache License Version 2.0</span></a></p><p align=\"center\"><br/></p><p align=\"center\">Thanks so much!</p><p align=\"center\"><br/></p></body></html>")
        self.a2license_text.setWordWrap(True)
        self.a2license_text.setOpenExternalLinks(True)
        self.a2license_text.setObjectName("a2license_text")
        self.verticalLayout_2.addWidget(self.a2license_text)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.license_layout.addWidget(self.scrollArea)
        QtCore.QMetaObject.connectSlotsByName(Form)
