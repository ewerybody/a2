# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2ctrl\a2module_list.ui'
#
# Created: Mon Aug 29 14:04:30 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ModuleList(object):
    def setupUi(self, ModuleList):
        ModuleList.setObjectName("ModuleList")
        ModuleList.resize(487, 889)
        self.module_list_layout = QtGui.QVBoxLayout(ModuleList)
        self.module_list_layout.setSpacing(5)
        self.module_list_layout.setContentsMargins(0, 5, 0, 0)
        self.module_list_layout.setObjectName("module_list_layout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton = QtGui.QToolButton(ModuleList)
        self.toolButton.setEnabled(False)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.lineEdit = QtGui.QLineEdit(ModuleList)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.module_list_layout.addLayout(self.horizontalLayout)
        self.list_widget = QtGui.QListWidget(ModuleList)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.list_widget.setIconSize(QtCore.QSize(32, 32))
        self.list_widget.setObjectName("list_widget")
        self.module_list_layout.addWidget(self.list_widget)

        self.retranslateUi(ModuleList)
        QtCore.QMetaObject.connectSlotsByName(ModuleList)

    def retranslateUi(self, ModuleList):
        ModuleList.setWindowTitle(QtGui.QApplication.translate("ModuleList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("ModuleList", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.list_widget.setSortingEnabled(True)

