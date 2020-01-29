# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2widget\a2module_list.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2widget\a2module_list.ui' applies.
#
# Created: Tue Jan 28 21:59:37 2020
#      by: pyside2-uic  running on PySide2 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ModuleList(object):
    def setupUi(self, ModuleList):
        ModuleList.setObjectName("ModuleList")
        ModuleList.resize(296, 759)
        self.module_list_layout = QtWidgets.QVBoxLayout(ModuleList)
        self.module_list_layout.setSpacing(5)
        self.module_list_layout.setContentsMargins(0, 5, 0, 0)
        self.module_list_layout.setObjectName("module_list_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search_field = QtWidgets.QLineEdit(ModuleList)
        self.search_field.setObjectName("search_field")
        self.horizontalLayout.addWidget(self.search_field)
        self.a2search_x_button = QtWidgets.QPushButton(ModuleList)
        self.a2search_x_button.setText("")
        self.a2search_x_button.setFlat(True)
        self.a2search_x_button.setObjectName("a2search_x_button")
        self.horizontalLayout.addWidget(self.a2search_x_button)
        self.filter_menu_button = A2MoreButton(ModuleList)
        self.filter_menu_button.setObjectName("filter_menu_button")
        self.horizontalLayout.addWidget(self.filter_menu_button)
        self.module_list_layout.addLayout(self.horizontalLayout)
        self.a2module_list_widget = A2List(ModuleList)
        self.a2module_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.a2module_list_widget.setAlternatingRowColors(True)
        self.a2module_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.a2module_list_widget.setObjectName("a2module_list_widget")
        self.module_list_layout.addWidget(self.a2module_list_widget)

        self.retranslateUi(ModuleList)
        QtCore.QMetaObject.connectSlotsByName(ModuleList)

    def retranslateUi(self, ModuleList):
        ModuleList.setWindowTitle(QtWidgets.QApplication.translate("ModuleList", "Form", None, -1))
        self.filter_menu_button.setText(QtWidgets.QApplication.translate("ModuleList", "...", None, -1))
        self.a2module_list_widget.setSortingEnabled(True)

from a2widget.a2list import A2List
from a2widget.a2more_button import A2MoreButton
