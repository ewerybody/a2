# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2module_source.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QToolButton, QVBoxLayout, QWidget
from a2qt.QtCore import QMetaObject, QSize, Qt
from a2qt.QtGui import QFont

from a2widget.a2more_button import A2MoreButton

class Ui_Form:
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName('Form')
        self.modsource_layout = QVBoxLayout(Form)
        self.modsource_layout.setContentsMargins(0, 0, 0, 0)
        self.modsource_layout.setObjectName('modsource_layout')
        self._check_layout = QHBoxLayout()
        self._check_layout.setSpacing(0)
        self._check_layout.setObjectName('_check_layout')
        self.check = QCheckBox(Form)
        self.check.setObjectName('check')
        self.check.setText('')
        self._check_layout.addWidget(self.check)
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(8)
        self.header_layout.setObjectName('header_layout')
        self.tool_button = QToolButton(Form)
        self.tool_button.setObjectName('tool_button')
        self.tool_button.setText('...')
        self.tool_button.setAutoRaise(True)
        self.tool_button.setArrowType(Qt.RightArrow)
        self.header_layout.addWidget(self.tool_button)
        self.icon_label = QLabel(Form)
        self.icon_label.setObjectName('icon_label')
        self.icon_label.setMinimumSize(QSize(20, 20))
        self.icon_label.setMaximumSize(QSize(20, 20))
        self.icon_label.setText('')
        self.icon_label.setTextFormat(Qt.PlainText)
        self.header_layout.addWidget(self.icon_label)
        self.mod_label = QLabel(Form)
        self.mod_label.setObjectName('mod_label')
        self.mod_label.setMinimumSize(QSize(40, 0))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.mod_label.setFont(font)
        self.mod_label.setText('ModSourceName')
        self.mod_label.setTextFormat(Qt.PlainText)
        self.header_layout.addWidget(self.mod_label)
        self.mod_count = QLabel(Form)
        self.mod_count.setObjectName('mod_count')
        self.mod_count.setText('TextLabel')
        self.mod_count.setTextFormat(Qt.PlainText)
        self.mod_count.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.mod_count)
        self.error_icon = QToolButton(Form)
        self.error_icon.setObjectName('error_icon')
        self.error_icon.setEnabled(False)
        self.error_icon.setText('...')
        self.error_icon.setAutoRaise(True)
        self.error_icon.setArrowType(Qt.NoArrow)
        self.header_layout.addWidget(self.error_icon)
        self._check_layout.addLayout(self.header_layout)
        self.a2option_button = A2MoreButton(Form)
        self.a2option_button.setObjectName('a2option_button')
        self.a2option_button.setText('')
        self.a2option_button.setAutoRaise(True)
        self._check_layout.addWidget(self.a2option_button)
        self._check_layout.setStretch(1, 1)
        self.modsource_layout.addLayout(self._check_layout)
        self.details_widget = QWidget(Form)
        self.details_widget.setObjectName('details_widget')
        self.modsource_layout.addWidget(self.details_widget)
        QMetaObject.connectSlotsByName(Form)
