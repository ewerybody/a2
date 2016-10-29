# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2widget\a2item_editor.ui'
#
# Created: Wed Oct 26 14:21:48 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_A2ItemEditor(object):
    def setupUi(self, A2ItemEditor):
        A2ItemEditor.setObjectName("A2ItemEditor")
        A2ItemEditor.resize(273, 431)
        self.item_editor_layout = QtGui.QHBoxLayout(A2ItemEditor)
        self.item_editor_layout.setObjectName("item_editor_layout")
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
        self.item_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.item_list.setObjectName("item_list")
        self.verticalLayout.addWidget(self.item_list)
        self.item_editor_layout.addLayout(self.verticalLayout)
        self.item_editor_layout.setStretch(0, 1)

        self.retranslateUi(A2ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(A2ItemEditor)

    def retranslateUi(self, A2ItemEditor):
        A2ItemEditor.setWindowTitle(QtGui.QApplication.translate("A2ItemEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.search_field.setPlaceholderText(QtGui.QApplication.translate("A2ItemEditor", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.add_entry_button.setText(QtGui.QApplication.translate("A2ItemEditor", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.del_entry_button.setText(QtGui.QApplication.translate("A2ItemEditor", "Remove", None, QtGui.QApplication.UnicodeUTF8))
