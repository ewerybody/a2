# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2widget\a2module_source.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2widget\a2module_source.ui' applies.
#
# Created: Tue Jan 28 21:59:37 2020
#      by: pyside2-uic  running on PySide2 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(524, 46)
        self.modsource_layout = QtWidgets.QVBoxLayout(Form)
        self.modsource_layout.setObjectName("modsource_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tool_button = QtWidgets.QToolButton(Form)
        self.tool_button.setText("...")
        self.tool_button.setAutoRaise(True)
        self.tool_button.setArrowType(QtCore.Qt.RightArrow)
        self.tool_button.setObjectName("tool_button")
        self.horizontalLayout.addWidget(self.tool_button)
        self.check = QtWidgets.QCheckBox(Form)
        self.check.setText("CheckBox")
        self.check.setObjectName("check")
        self.horizontalLayout.addWidget(self.check)
        self.mod_count = QtWidgets.QLabel(Form)
        self.mod_count.setText("TextLabel")
        self.mod_count.setObjectName("mod_count")
        self.horizontalLayout.addWidget(self.mod_count)
        self.error_icon = QtWidgets.QToolButton(Form)
        self.error_icon.setEnabled(False)
        self.error_icon.setText("...")
        self.error_icon.setAutoRaise(True)
        self.error_icon.setArrowType(QtCore.Qt.NoArrow)
        self.error_icon.setObjectName("error_icon")
        self.horizontalLayout.addWidget(self.error_icon)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.modsource_layout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

