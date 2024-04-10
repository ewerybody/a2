# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2item_editor.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import (QHBoxLayout, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget)
from a2qt.QtCore import QCoreApplication, QMetaObject

from a2widget.a2list import A2List

class Ui_A2ItemEditor:
    def setupUi(self, A2ItemEditor):
        if not A2ItemEditor.objectName():
            A2ItemEditor.setObjectName('A2ItemEditor')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(A2ItemEditor.sizePolicy().hasHeightForWidth())
        A2ItemEditor.setSizePolicy(sizePolicy)
        self.item_editor_layout = QHBoxLayout(A2ItemEditor)
        self.item_editor_layout.setContentsMargins(0, 0, 0, 0)
        self.item_editor_layout.setObjectName('item_editor_layout')
        self.list_layout_widget = QWidget(A2ItemEditor)
        self.list_layout_widget.setObjectName('list_layout_widget')
        self.list_layout = QVBoxLayout(self.list_layout_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setObjectName('list_layout')
        self.search_field_layout = QHBoxLayout()
        self.search_field_layout.setObjectName('search_field_layout')
        self.search_field = QLineEdit(self.list_layout_widget)
        self.search_field.setObjectName('search_field')
        self.search_field.setInputMask('')
        self.search_field_layout.addWidget(self.search_field)
        self.a2search_x_button = QPushButton(self.list_layout_widget)
        self.a2search_x_button.setObjectName('a2search_x_button')
        self.a2search_x_button.setFlat(True)
        self.search_field_layout.addWidget(self.a2search_x_button)
        self.list_layout.addLayout(self.search_field_layout)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName('buttons_layout')
        self.a2item_editor_add_button = QPushButton(self.list_layout_widget)
        self.a2item_editor_add_button.setObjectName('a2item_editor_add_button')
        self.a2item_editor_add_button.setText('Add')
        self.buttons_layout.addWidget(self.a2item_editor_add_button)
        self.a2item_editor_remove_button = QPushButton(self.list_layout_widget)
        self.a2item_editor_remove_button.setObjectName('a2item_editor_remove_button')
        self.a2item_editor_remove_button.setEnabled(False)
        self.a2item_editor_remove_button.setText('Remove')
        self.buttons_layout.addWidget(self.a2item_editor_remove_button)
        self.buttons_layout.setStretch(0, 1)
        self.list_layout.addLayout(self.buttons_layout)
        self.item_list = A2List(self.list_layout_widget)
        self.item_list.setObjectName('item_list')
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.item_list.sizePolicy().hasHeightForWidth())
        self.item_list.setSizePolicy(sizePolicy1)
        self.item_list.setAlternatingRowColors(True)
        self.list_layout.addWidget(self.item_list)
        self.item_editor_layout.addWidget(self.list_layout_widget)
        self.config_widget = QWidget(A2ItemEditor)
        self.config_widget.setObjectName('config_widget')
        self.config_widget.setEnabled(False)
        self.item_editor_layout.addWidget(self.config_widget)
        self.item_editor_layout.setStretch(1, 5)
        self.retranslateUi(A2ItemEditor)
        QMetaObject.connectSlotsByName(A2ItemEditor)
    def retranslateUi(self, A2ItemEditor):
        self.search_field.setPlaceholderText(QCoreApplication.translate('A2ItemEditor', 'search', None))
        self.a2search_x_button.setText("")
