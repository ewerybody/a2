# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'button_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

from a2widget.local_script import ScriptSelector

class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(671, 101)
        edit.setWindowTitle(u"Form")
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName(u"displayLabelLabel")
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setText(u"label text")
        self.displayLabelLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.displayLabelLabel)

        self.cfg_labeltext = QLineEdit(edit)
        self.cfg_labeltext.setObjectName(u"cfg_labeltext")
        self.cfg_labeltext.setText(u"")
        self.cfg_labeltext.setPlaceholderText(u"Space used by Button if empty!")

        self.edit_layout.setWidget(0, QFormLayout.FieldRole, self.cfg_labeltext)

        self.displayLabelLabel_2 = QLabel(edit)
        self.displayLabelLabel_2.setObjectName(u"displayLabelLabel_2")
        self.displayLabelLabel_2.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_2.setText(u"button text")
        self.displayLabelLabel_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(1, QFormLayout.LabelRole, self.displayLabelLabel_2)

        self.cfg_buttontext = QLineEdit(edit)
        self.cfg_buttontext.setObjectName(u"cfg_buttontext")
        self.cfg_buttontext.setPlaceholderText(u"Text to show on the Button.")

        self.edit_layout.setWidget(1, QFormLayout.FieldRole, self.cfg_buttontext)

        self.displayLabelLabel_3 = QLabel(edit)
        self.displayLabelLabel_3.setObjectName(u"displayLabelLabel_3")
        self.displayLabelLabel_3.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_3.setText(u"python script")
        self.displayLabelLabel_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.displayLabelLabel_3)

        self.script_selector = ScriptSelector(edit)
        self.script_selector.setObjectName(u"script_selector")

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.script_selector)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        pass
    # retranslateUi

