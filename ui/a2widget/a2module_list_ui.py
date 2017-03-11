# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2module_list.ui'
#
# Created: Sat Mar 11 01:59:29 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ModuleList(object):
    def setupUi(self, ModuleList):
        ModuleList.setObjectName("ModuleList")
        ModuleList.resize(296, 759)
        self.module_list_layout = QtGui.QVBoxLayout(ModuleList)
        self.module_list_layout.setSpacing(5)
        self.module_list_layout.setContentsMargins(0, 5, 0, 0)
        self.module_list_layout.setObjectName("module_list_layout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filter_menu_button = QtGui.QToolButton(ModuleList)
        self.filter_menu_button.setObjectName("filter_menu_button")
        self.horizontalLayout.addWidget(self.filter_menu_button)
        self.search_field = QtGui.QLineEdit(ModuleList)
        self.search_field.setObjectName("search_field")
        self.horizontalLayout.addWidget(self.search_field)
        self.a2search_x_button = QtGui.QPushButton(ModuleList)
        self.a2search_x_button.setText("")
        self.a2search_x_button.setFlat(True)
        self.a2search_x_button.setObjectName("a2search_x_button")
        self.horizontalLayout.addWidget(self.a2search_x_button)
        self.module_list_layout.addLayout(self.horizontalLayout)
        self.a2module_list_widget = QtGui.QListWidget(ModuleList)
        self.a2module_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.a2module_list_widget.setAlternatingRowColors(True)
        self.a2module_list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.a2module_list_widget.setObjectName("a2module_list_widget")
        self.module_list_layout.addWidget(self.a2module_list_widget)

        self.retranslateUi(ModuleList)
        QtCore.QMetaObject.connectSlotsByName(ModuleList)

    def retranslateUi(self, ModuleList):
        ModuleList.setWindowTitle(QtGui.QApplication.translate("ModuleList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_menu_button.setText(QtGui.QApplication.translate("ModuleList", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.a2module_list_widget.setSortingEnabled(True)

