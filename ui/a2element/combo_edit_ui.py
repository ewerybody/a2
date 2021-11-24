# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'combo_edit.ui'

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
from a2qt.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidgetItem,
    QSizePolicy, QToolButton, QVBoxLayout, QWidget)

from a2widget.a2list import A2List
from a2widget.a2text_field import A2InternalName

class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName(u"cfg_name")
        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")
        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_label)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(edit)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.verticalLayout.addWidget(self.label_6)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(40, 0, -1, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.plus_button = QToolButton(edit)
        self.plus_button.setObjectName(u"plus_button")
        self.plus_button.setMaximumSize(QSize(50, 50))
        self.plus_button.setAutoRaise(True)
        self.verticalLayout_2.addWidget(self.plus_button)
        self.minus_button = QToolButton(edit)
        self.minus_button.setObjectName(u"minus_button")
        self.minus_button.setMaximumSize(QSize(50, 50))
        self.minus_button.setAutoRaise(True)
        self.verticalLayout_2.addWidget(self.minus_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.edit_layout.setLayout(2, QFormLayout.LabelRole, self.verticalLayout)
        self.cfg_items = A2List(edit)
        self.cfg_items.setObjectName(u"cfg_items")
        self.cfg_items.setMaximumSize(QSize(16777215, 145))
        self.cfg_items.setAlternatingRowColors(True)
        self.cfg_items.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_items)
        self.cfg_user_edit = QCheckBox(edit)
        self.cfg_user_edit.setObjectName(u"cfg_user_edit")
        self.edit_layout.setWidget(3, QFormLayout.FieldRole, self.cfg_user_edit)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)
    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_combobox1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"some values", None))
        self.label_6.setText(QCoreApplication.translate("edit", u"items:", None))
        self.cfg_user_edit.setText(QCoreApplication.translate("edit", u"allow user edit", None))
