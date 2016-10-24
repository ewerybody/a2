# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2widget\a2item_editor.ui'
#
# Created: Mon Oct 24 22:55:04 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_A2ItemEditor(object):
    def setupUi(self, A2ItemEditor):
        A2ItemEditor.setObjectName("A2ItemEditor")
        A2ItemEditor.resize(726, 731)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(A2ItemEditor)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.search_field = QtGui.QLineEdit(A2ItemEditor)
        self.search_field.setObjectName("search_field")
        self.verticalLayout.addWidget(self.search_field)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_entry_button = QtGui.QPushButton(A2ItemEditor)
        self.add_entry_button.setObjectName("add_entry_button")
        self.horizontalLayout.addWidget(self.add_entry_button)
        self.del_entry_button = QtGui.QPushButton(A2ItemEditor)
        self.del_entry_button.setObjectName("del_entry_button")
        self.horizontalLayout.addWidget(self.del_entry_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.item_list = QtGui.QListWidget(A2ItemEditor)
        self.item_list.setObjectName("item_list")
        self.verticalLayout.addWidget(self.item_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.horizontalLayout_2.setStretch(0, 1)

        self.retranslateUi(A2ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(A2ItemEditor)

    def retranslateUi(self, A2ItemEditor):
        A2ItemEditor.setWindowTitle(QtGui.QApplication.translate("A2ItemEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.search_field.setPlaceholderText(QtGui.QApplication.translate("A2ItemEditor", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.add_entry_button.setText(QtGui.QApplication.translate("A2ItemEditor", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.del_entry_button.setText(QtGui.QApplication.translate("A2ItemEditor", "Remove", None, QtGui.QApplication.UnicodeUTF8))

