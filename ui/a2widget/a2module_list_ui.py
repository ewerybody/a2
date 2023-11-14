# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2module_list.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import (QAbstractItemView, QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTreeWidgetItem, QVBoxLayout)
from a2qt.QtCore import Property, QMetaObject, Qt

from a2widget.a2modlist import A2ModList
from a2widget.a2more_button import A2MoreButton

class Ui_ModuleList:
    def setupUi(self, ModuleList):
        if not ModuleList.objectName():
            ModuleList.setObjectName('ModuleList')
        ModuleList.setWindowTitle('Form')
        self.module_list_layout = QVBoxLayout(ModuleList)
        self.module_list_layout.setObjectName('module_list_layout')
        self.module_list_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.search_field = QLineEdit(ModuleList)
        self.search_field.setObjectName('search_field')
        self.horizontalLayout.addWidget(self.search_field)
        self.a2search_x_button = QPushButton(ModuleList)
        self.a2search_x_button.setObjectName('a2search_x_button')
        self.a2search_x_button.setFlat(True)
        self.horizontalLayout.addWidget(self.a2search_x_button)
        self.filter_menu_button = A2MoreButton(ModuleList)
        self.filter_menu_button.setObjectName('filter_menu_button')
        self.horizontalLayout.addWidget(self.filter_menu_button)
        self.module_list_layout.addLayout(self.horizontalLayout)
        self.a2modlist_label_group = QGroupBox(ModuleList)
        self.a2modlist_label_group.setObjectName('a2modlist_label_group')
        self.a2modlist_label_group.setStyleSheet('b')
        self.verticalLayout = QVBoxLayout(self.a2modlist_label_group)
        self.verticalLayout.setObjectName('verticalLayout')
        self.label = QLabel(self.a2modlist_label_group)
        self.label.setObjectName('label')
        self.label.setText('')
        self.verticalLayout.addWidget(self.label)
        self.module_list_layout.addWidget(self.a2modlist_label_group)
        self.a2module_list_widget = A2ModList(ModuleList)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.a2module_list_widget.setHeaderItem(__qtreewidgetitem)
        self.a2module_list_widget.setObjectName('a2module_list_widget')
        self.a2module_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.a2module_list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.a2module_list_widget.setProperty("showDropIndicator", False)
        self.a2module_list_widget.setAlternatingRowColors(True)
        self.a2module_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.a2module_list_widget.setIndentation(0)
        self.a2module_list_widget.setAnimated(True)
        self.a2module_list_widget.setColumnCount(1)
        self.a2module_list_widget.header().setVisible(False)
        self.module_list_layout.addWidget(self.a2module_list_widget)
        self.retranslateUi(ModuleList)
        QMetaObject.connectSlotsByName(ModuleList)
    def retranslateUi(self, ModuleList):
        self.a2modlist_label_group.setTitle("")
