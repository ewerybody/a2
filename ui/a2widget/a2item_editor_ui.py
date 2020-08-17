# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2widget\a2item_editor.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2widget\a2item_editor.ui' applies.
#
# Created: Mon Aug 17 17:54:55 2020
#      by: pyside2-uic  running on PySide2 5.15.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_A2ItemEditor(object):
    def setupUi(self, A2ItemEditor):
        A2ItemEditor.setObjectName("A2ItemEditor")
        A2ItemEditor.resize(1069, 653)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(A2ItemEditor.sizePolicy().hasHeightForWidth())
        A2ItemEditor.setSizePolicy(sizePolicy)
        self.item_editor_layout = QtWidgets.QHBoxLayout(A2ItemEditor)
        self.item_editor_layout.setObjectName("item_editor_layout")
        self.list_layout_widget = QtWidgets.QWidget(A2ItemEditor)
        self.list_layout_widget.setObjectName("list_layout_widget")
        self.list_layout = QtWidgets.QVBoxLayout(self.list_layout_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setObjectName("list_layout")
        self.search_field_layout = QtWidgets.QHBoxLayout()
        self.search_field_layout.setContentsMargins(0, 0, 0, 0)
        self.search_field_layout.setObjectName("search_field_layout")
        self.search_field = QtWidgets.QLineEdit(self.list_layout_widget)
        self.search_field.setInputMask("")
        self.search_field.setObjectName("search_field")
        self.search_field_layout.addWidget(self.search_field)
        self.a2search_x_button = QtWidgets.QPushButton(self.list_layout_widget)
        self.a2search_x_button.setText("")
        self.a2search_x_button.setFlat(True)
        self.a2search_x_button.setObjectName("a2search_x_button")
        self.search_field_layout.addWidget(self.a2search_x_button)
        self.list_layout.addLayout(self.search_field_layout)
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        self.a2item_editor_add_button = QtWidgets.QPushButton(self.list_layout_widget)
        self.a2item_editor_add_button.setText("Add")
        self.a2item_editor_add_button.setObjectName("a2item_editor_add_button")
        self.buttons_layout.addWidget(self.a2item_editor_add_button)
        self.a2item_editor_remove_button = QtWidgets.QPushButton(self.list_layout_widget)
        self.a2item_editor_remove_button.setEnabled(False)
        self.a2item_editor_remove_button.setText("Remove")
        self.a2item_editor_remove_button.setObjectName("a2item_editor_remove_button")
        self.buttons_layout.addWidget(self.a2item_editor_remove_button)
        self.buttons_layout.setStretch(0, 1)
        self.list_layout.addLayout(self.buttons_layout)
        self.item_list = A2List(self.list_layout_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_list.sizePolicy().hasHeightForWidth())
        self.item_list.setSizePolicy(sizePolicy)
        self.item_list.setAlternatingRowColors(True)
        self.item_list.setObjectName("item_list")
        self.list_layout.addWidget(self.item_list)
        self.item_editor_layout.addWidget(self.list_layout_widget)
        self.config_widget = QtWidgets.QWidget(A2ItemEditor)
        self.config_widget.setEnabled(False)
        self.config_widget.setObjectName("config_widget")
        self.item_editor_layout.addWidget(self.config_widget)
        self.item_editor_layout.setStretch(1, 5)

        self.retranslateUi(A2ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(A2ItemEditor)

    def retranslateUi(self, A2ItemEditor):
        self.search_field.setPlaceholderText(QtWidgets.QApplication.translate("A2ItemEditor", "search", None, -1))

from a2widget.a2list import A2List
