# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2module_source.ui'

Created by: Qt User Interface Compiler version 6.2.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from a2qt.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from a2qt.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

class Ui_Form:
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.modsource_layout = QVBoxLayout(Form)
        self.modsource_layout.setContentsMargins(0, 0, 0, 0)
        self.modsource_layout.setObjectName(u"modsource_layout")
        self.header_layout = QHBoxLayout()
        self.header_layout.setObjectName(u"header_layout")
        self.check = QCheckBox(Form)
        self.check.setObjectName(u"check")
        self.check.setText(u"")
        self.header_layout.addWidget(self.check)
        self.tool_button = QToolButton(Form)
        self.tool_button.setObjectName(u"tool_button")
        self.tool_button.setText(u"...")
        self.tool_button.setAutoRaise(True)
        self.tool_button.setArrowType(Qt.RightArrow)
        self.header_layout.addWidget(self.tool_button)
        self.label_widget = QWidget(Form)
        self.label_widget.setObjectName(u"label_widget")
        self.horizontalLayout_2 = QHBoxLayout(self.label_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.icon_label = QLabel(self.label_widget)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setMinimumSize(QSize(20, 20))
        self.icon_label.setMaximumSize(QSize(20, 20))
        self.icon_label.setText(u"")
        self.horizontalLayout_2.addWidget(self.icon_label)
        self.mod_label = QLabel(self.label_widget)
        self.mod_label.setObjectName(u"mod_label")
        self.mod_label.setMinimumSize(QSize(40, 0))
        font = QFont()
        font.setBold(False)
        self.mod_label.setFont(font)
        self.mod_label.setText(u"ModSourceName")
        self.horizontalLayout_2.addWidget(self.mod_label)
        self.mod_count = QLabel(self.label_widget)
        self.mod_count.setObjectName(u"mod_count")
        self.mod_count.setText(u"TextLabel")
        self.mod_count.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_2.addWidget(self.mod_count)
        self.header_layout.addWidget(self.label_widget)
        self.error_icon = QToolButton(Form)
        self.error_icon.setObjectName(u"error_icon")
        self.error_icon.setEnabled(False)
        self.error_icon.setText(u"...")
        self.error_icon.setAutoRaise(True)
        self.error_icon.setArrowType(Qt.NoArrow)
        self.header_layout.addWidget(self.error_icon)
        self.header_layout.setStretch(2, 1)
        self.modsource_layout.addLayout(self.header_layout)
        self.details_widget = QWidget(Form)
        self.details_widget.setObjectName(u"details_widget")
        self.modsource_layout.addWidget(self.details_widget)
        QMetaObject.connectSlotsByName(Form)
