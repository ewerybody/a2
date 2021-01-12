# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2module_list.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2more_button import A2MoreButton
from a2widget.a2list import A2List


class Ui_ModuleList(object):
    def setupUi(self, ModuleList):
        if not ModuleList.objectName():
            ModuleList.setObjectName(u"ModuleList")

        self.module_list_layout = QVBoxLayout(ModuleList)
        self.module_list_layout.setSpacing(5)
        self.module_list_layout.setObjectName(u"module_list_layout")
        self.module_list_layout.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_field = QLineEdit(ModuleList)
        self.search_field.setObjectName(u"search_field")

        self.horizontalLayout.addWidget(self.search_field)

        self.a2search_x_button = QPushButton(ModuleList)
        self.a2search_x_button.setObjectName(u"a2search_x_button")
        self.a2search_x_button.setFlat(True)

        self.horizontalLayout.addWidget(self.a2search_x_button)

        self.filter_menu_button = A2MoreButton(ModuleList)
        self.filter_menu_button.setObjectName(u"filter_menu_button")

        self.horizontalLayout.addWidget(self.filter_menu_button)


        self.module_list_layout.addLayout(self.horizontalLayout)

        self.a2module_list_widget = A2List(ModuleList)
        self.a2module_list_widget.setObjectName(u"a2module_list_widget")
        self.a2module_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.a2module_list_widget.setAlternatingRowColors(True)
        self.a2module_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.a2module_list_widget.setSortingEnabled(True)

        self.module_list_layout.addWidget(self.a2module_list_widget)


        self.retranslateUi(ModuleList)

        QMetaObject.connectSlotsByName(ModuleList)
    # setupUi

    def retranslateUi(self, ModuleList):
        ModuleList.setWindowTitle(QCoreApplication.translate("ModuleList", u"Form", None))
        self.a2search_x_button.setText("")
        self.filter_menu_button.setText(QCoreApplication.translate("ModuleList", u"...", None))
    # retranslateUi

