# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'group_edit.ui'

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
from a2qt.QtWidgets import (QApplication, QCheckBox, QFormLayout, QLabel,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

from a2widget.a2text_field import A2InternalName

class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        self.edit_layout = QVBoxLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.edit_layout.setContentsMargins(-1, -1, 0, -1)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setHorizontalSpacing(5)
        self.formLayout.setVerticalSpacing(5)
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setMaximumSize(QSize(16777215, 16777215))
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = A2InternalName(edit)
        self.cfg_name.setObjectName(u"cfg_name")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setMaximumSize(QSize(16777215, 16777215))
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QLineEdit(edit)
        self.cfg_label.setObjectName(u"cfg_label")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cfg_label)
        self.cfg_disablable = QCheckBox(edit)
        self.cfg_disablable.setObjectName(u"cfg_disablable")
        self.cfg_disablable.setChecked(True)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cfg_disablable)
        self.cfg_enabled = QCheckBox(edit)
        self.cfg_enabled.setObjectName(u"cfg_enabled")
        self.cfg_enabled.setChecked(True)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cfg_enabled)
        self.edit_layout.addLayout(self.formLayout)
        self.retranslateUi(edit)
        QMetaObject.connectSlotsByName(edit)
    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_group1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"some group name", None))
        self.cfg_disablable.setText(QCoreApplication.translate("edit", u"checkable", None))
        self.cfg_enabled.setText(QCoreApplication.translate("edit", u"enabled by default", None))
