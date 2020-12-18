# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pathlist_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_edit(object):
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName(u"edit")
        edit.resize(549, 124)
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName(u"edit_layout")
        self.internalNameLabel = QLabel(edit)
        self.internalNameLabel.setObjectName(u"internalNameLabel")
        self.internalNameLabel.setMinimumSize(QSize(100, 0))
        self.internalNameLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(0, QFormLayout.LabelRole, self.internalNameLabel)

        self.cfg_name = QLineEdit(edit)
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

        self.cfg_max_items = QSpinBox(edit)
        self.cfg_max_items.setObjectName(u"cfg_max_items")
        self.cfg_max_items.setSuffix(u"")
        self.cfg_max_items.setPrefix(u"")
        self.cfg_max_items.setMinimum(1)
        self.cfg_max_items.setMaximum(99)

        self.edit_layout.setWidget(2, QFormLayout.FieldRole, self.cfg_max_items)

        self.maxItemsLabel = QLabel(edit)
        self.maxItemsLabel.setObjectName(u"maxItemsLabel")
        self.maxItemsLabel.setMinimumSize(QSize(100, 0))
        self.maxItemsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(2, QFormLayout.LabelRole, self.maxItemsLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.cfg_browse_type_0 = QRadioButton(edit)
        self.cfg_browse_type_0.setObjectName(u"cfg_browse_type_0")
        self.cfg_browse_type_0.setChecked(True)

        self.horizontalLayout_2.addWidget(self.cfg_browse_type_0)

        self.cfg_browse_type_1 = QRadioButton(edit)
        self.cfg_browse_type_1.setObjectName(u"cfg_browse_type_1")

        self.horizontalLayout_2.addWidget(self.cfg_browse_type_1)

        self.horizontalLayout_2.setStretch(1, 1)

        self.edit_layout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_3 = QLabel(edit)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.edit_layout.setWidget(3, QFormLayout.LabelRole, self.label_3)


        self.retranslateUi(edit)

        QMetaObject.connectSlotsByName(edit)
    # setupUi

    def retranslateUi(self, edit):
        edit.setWindowTitle(QCoreApplication.translate("edit", u"Form", None))
        self.internalNameLabel.setText(QCoreApplication.translate("edit", u"internal name:", None))
        self.cfg_name.setText(QCoreApplication.translate("edit", u"extensionX_path1", None))
        self.displayLabelLabel.setText(QCoreApplication.translate("edit", u"display label:", None))
        self.cfg_label.setText(QCoreApplication.translate("edit", u"some pathlist bla", None))
        self.maxItemsLabel.setText(QCoreApplication.translate("edit", u"max items:", None))
        self.cfg_browse_type_0.setText(QCoreApplication.translate("edit", u"folder", None))
        self.cfg_browse_type_1.setText(QCoreApplication.translate("edit", u"file", None))
        self.label_3.setText(QCoreApplication.translate("edit", u"type:", None))
    # retranslateUi

