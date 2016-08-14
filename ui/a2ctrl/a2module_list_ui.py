# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2ctrl\a2module_list.ui'
#
# Created: Sun Aug 14 22:58:13 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ModuleList(object):
    def setupUi(self, ModuleList):
        ModuleList.setObjectName("ModuleList")
        ModuleList.resize(475, 860)
        self.module_list_layout = QtGui.QVBoxLayout(ModuleList)
        self.module_list_layout.setObjectName("module_list_layout")
        self.module_box = QtGui.QGroupBox(ModuleList)
        self.module_box.setTitle("")
        self.module_box.setObjectName("module_box")
        self.verticalLayout = QtGui.QVBoxLayout(self.module_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton = QtGui.QToolButton(self.module_box)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.lineEdit = QtGui.QLineEdit(self.module_box)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.list_widget = QtGui.QListWidget(self.module_box)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.list_widget.setIconSize(QtCore.QSize(32, 32))
        self.list_widget.setObjectName("list_widget")
        self.verticalLayout.addWidget(self.list_widget)
        self.module_list_layout.addWidget(self.module_box)

        self.retranslateUi(ModuleList)
        QtCore.QMetaObject.connectSlotsByName(ModuleList)

    def retranslateUi(self, ModuleList):
        ModuleList.setWindowTitle(QtGui.QApplication.translate("ModuleList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("ModuleList", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.list_widget.setSortingEnabled(True)

