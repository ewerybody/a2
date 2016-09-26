# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2widget\a2item_editor.ui'
#
# Created: Mon Sep 26 09:56:27 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(726, 808)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.search_field = QtGui.QLineEdit(Form)
        self.search_field.setObjectName("search_field")
        self.verticalLayout.addWidget(self.search_field)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_entry_button = QtGui.QPushButton(Form)
        self.add_entry_button.setObjectName("add_entry_button")
        self.horizontalLayout.addWidget(self.add_entry_button)
        self.del_entry_button = QtGui.QPushButton(Form)
        self.del_entry_button.setObjectName("del_entry_button")
        self.horizontalLayout.addWidget(self.del_entry_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.list = QtGui.QListView(Form)
        self.list.setObjectName("list")
        self.verticalLayout.addWidget(self.list)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.config_layout = QtGui.QVBoxLayout()
        self.config_layout.setObjectName("config_layout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.entry_name = QtGui.QLineEdit(Form)
        self.entry_name.setObjectName("entry_name")
        self.horizontalLayout_3.addWidget(self.entry_name)
        self.config_layout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.config_layout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.config_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.search_field.setPlaceholderText(QtGui.QApplication.translate("Form", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.add_entry_button.setText(QtGui.QApplication.translate("Form", "Add Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.del_entry_button.setText(QtGui.QApplication.translate("Form", "Remove Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Entry Name", None, QtGui.QApplication.UnicodeUTF8))

