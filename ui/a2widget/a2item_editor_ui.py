# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2item_editor.ui'
#
# Created: Mon Oct 24 14:22:23 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
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
        self.config_layout = QtGui.QVBoxLayout()
        self.config_layout.setObjectName("config_layout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(A2ItemEditor)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.entry_name = QtGui.QLineEdit(A2ItemEditor)
        self.entry_name.setObjectName("entry_name")
        self.horizontalLayout_3.addWidget(self.entry_name)
        self.config_layout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.config_layout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.config_layout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.retranslateUi(A2ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(A2ItemEditor)

    def retranslateUi(self, A2ItemEditor):
        A2ItemEditor.setWindowTitle(QtGui.QApplication.translate("A2ItemEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.search_field.setPlaceholderText(QtGui.QApplication.translate("A2ItemEditor", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.add_entry_button.setText(QtGui.QApplication.translate("A2ItemEditor", "Add Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.del_entry_button.setText(QtGui.QApplication.translate("A2ItemEditor", "Remove Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("A2ItemEditor", "Entry Name", None, QtGui.QApplication.UnicodeUTF8))

