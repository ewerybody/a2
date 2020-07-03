# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file:
#   'c:\Users\eric\io\code\a2\ui\a2widget\a2item_editor.ui'
# licensing of that file applies.
#
# Created: Fri Jul  3 18:27:41 2020
#      by: pyside2-uic  running on PySide2 5.15.0
#
# pylint: disable=W0201,C0103,C0111
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_A2ItemEditor:
    def setupUi(self, A2ItemEditor):
        A2ItemEditor.setObjectName("A2ItemEditor")
        A2ItemEditor.resize(910, 653)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(A2ItemEditor.sizePolicy().hasHeightForWidth())
        A2ItemEditor.setSizePolicy(sizePolicy)
        self.item_editor_layout = QtWidgets.QHBoxLayout(A2ItemEditor)
        self.item_editor_layout.setObjectName("item_editor_layout")
        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setObjectName("list_layout")
        self.search_field_layout = QtWidgets.QHBoxLayout()
        self.search_field_layout.setObjectName("search_field_layout")
        self.search_field = QtWidgets.QLineEdit(A2ItemEditor)
        self.search_field.setObjectName("search_field")
        self.search_field_layout.addWidget(self.search_field)
        self.a2search_x_button = QtWidgets.QPushButton(A2ItemEditor)
        self.a2search_x_button.setText("")
        self.a2search_x_button.setFlat(True)
        self.a2search_x_button.setObjectName("a2search_x_button")
        self.search_field_layout.addWidget(self.a2search_x_button)
        self.list_layout.addLayout(self.search_field_layout)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        self.a2item_editor_add_button = QtWidgets.QPushButton(A2ItemEditor)
        self.a2item_editor_add_button.setObjectName("a2item_editor_add_button")
        self.buttons_layout.addWidget(self.a2item_editor_add_button)
        self.a2item_editor_remove_button = QtWidgets.QPushButton(A2ItemEditor)
        self.a2item_editor_remove_button.setEnabled(False)
        self.a2item_editor_remove_button.setObjectName("a2item_editor_remove_button")
        self.buttons_layout.addWidget(self.a2item_editor_remove_button)
        self.buttons_layout.setStretch(0, 1)
        self.list_layout.addLayout(self.buttons_layout)
        self.item_list = A2List(A2ItemEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_list.sizePolicy().hasHeightForWidth())
        self.item_list.setSizePolicy(sizePolicy)
        self.item_list.setAlternatingRowColors(True)
        self.item_list.setObjectName("item_list")
        self.list_layout.addWidget(self.item_list)
        self.item_editor_layout.addLayout(self.list_layout)
        self.config_widget = QtWidgets.QWidget(A2ItemEditor)
        self.config_widget.setEnabled(False)
        self.config_widget.setObjectName("config_widget")
        self.item_editor_layout.addWidget(self.config_widget)
        self.item_editor_layout.setStretch(0, 1)
        self.item_editor_layout.setStretch(1, 3)

        self.retranslateUi(A2ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(A2ItemEditor)

    def retranslateUi(self, A2ItemEditor):
        A2ItemEditor.setWindowTitle(QtWidgets.QApplication.translate("A2ItemEditor", "Form", None, -1))
        self.search_field.setPlaceholderText(QtWidgets.QApplication.translate("A2ItemEditor", "search", None, -1))
        self.a2item_editor_add_button.setText(QtWidgets.QApplication.translate("A2ItemEditor", "Add", None, -1))
        self.a2item_editor_remove_button.setText(QtWidgets.QApplication.translate("A2ItemEditor", "Remove", None, -1))

from a2widget.a2list import A2List
