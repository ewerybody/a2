# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2item_editor.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2item_editor.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_A2ItemEditor(object):
    def setupUi(self, A2ItemEditor):
        A2ItemEditor.setObjectName("A2ItemEditor")
        A2ItemEditor.resize(697, 448)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(A2ItemEditor.sizePolicy().hasHeightForWidth())
        A2ItemEditor.setSizePolicy(sizePolicy)
        self.item_editor_layout = QtWidgets.QHBoxLayout(A2ItemEditor)
        self.item_editor_layout.setObjectName("item_editor_layout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_field = QtWidgets.QLineEdit(A2ItemEditor)
        self.search_field.setObjectName("search_field")
        self.horizontalLayout_2.addWidget(self.search_field)
        self.a2search_x_button = QtWidgets.QPushButton(A2ItemEditor)
        self.a2search_x_button.setText("")
        self.a2search_x_button.setFlat(True)
        self.a2search_x_button.setObjectName("a2search_x_button")
        self.horizontalLayout_2.addWidget(self.a2search_x_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_entry_button = QtWidgets.QPushButton(A2ItemEditor)
        self.add_entry_button.setObjectName("add_entry_button")
        self.horizontalLayout.addWidget(self.add_entry_button)
        self.del_entry_button = QtWidgets.QPushButton(A2ItemEditor)
        self.del_entry_button.setEnabled(False)
        self.del_entry_button.setObjectName("del_entry_button")
        self.horizontalLayout.addWidget(self.del_entry_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.item_list = QtWidgets.QListWidget(A2ItemEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_list.sizePolicy().hasHeightForWidth())
        self.item_list.setSizePolicy(sizePolicy)
        self.item_list.setAlternatingRowColors(True)
        self.item_list.setObjectName("item_list")
        self.verticalLayout.addWidget(self.item_list)
        self.item_editor_layout.addLayout(self.verticalLayout)
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
        self.add_entry_button.setText(QtWidgets.QApplication.translate("A2ItemEditor", "Add", None, -1))
        self.del_entry_button.setText(QtWidgets.QApplication.translate("A2ItemEditor", "Remove", None, -1))

