# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2licenses_widget.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2licenses_widget.ui' applies.
#
# Created: Tue Jan 15 09:41:10 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 688)
        self.license_layout = QtWidgets.QVBoxLayout(Form)
        self.license_layout.setObjectName("license_layout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 458, 666))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.a2license_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.a2license_text.setAccessibleDescription("")
        self.a2license_text.setAutoFillBackground(False)
        self.a2license_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.a2license_text.setWordWrap(True)
        self.a2license_text.setOpenExternalLinks(True)
        self.a2license_text.setObjectName("a2license_text")
        self.verticalLayout_2.addWidget(self.a2license_text)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.license_layout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.a2license_text.setText(QtWidgets.QApplication.translate("Form", "<html><head/><body><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_ahk.png\"/><br/><span style=\" font-weight:600;\">AutoHotkey</span> - a scripting language for desktop automation</p><p align=\"center\"><a href=\"https://autohotkey.com\"><span style=\" text-decoration: underline; color:#0000ff;\">autohotkey.com</span></a> - GNU GPLv2</p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_python.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Python</span> - high-level programming language</p><p align=\"center\"><a href=\"https://www.python.org/\"><span style=\" text-decoration: underline; color:#0000ff;\">python.org</span></a> - Python Software Foundation License - GPL compatible</p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_pyside.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Qt for Python</span> - Python binding of the cross-platform GUI toolkit Qt</p><p align=\"center\"><a href=\"https://www.qt.io/qt-for-python\"><span style=\" text-decoration: underline; color:#0000ff;\">qt.io/qt-for-python</span></a> - LGPLv3/GPLv2</p><p align=\"center\"><br/></p><p align=\"center\"><img src=\"res/logo_material.png\"/></p><p align=\"center\"><span style=\" font-weight:600;\">Material Icons</span> - Material Design icons by Google</p><p align=\"center\"><a href=\"https://material.io/icons\"><span style=\" text-decoration: underline; color:#0000ff;\">material.io/icons</span></a> - Apache License Version 2.0</p><p align=\"center\"><br/></p><p align=\"center\">Thanks so much!</p><p align=\"center\">...</p></body></html>", None, -1))

