# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\combo_edit.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2element\combo_edit.ui' applies.
#
# Created: Fri Nov 30 14:45:43 2018
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(407, 309)
        self.edit_layout = QtWidgets.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setObjectName("edit_layout")
        self.internalNameLabel = QtWidgets.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtWidgets.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QtWidgets.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtWidgets.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_label)
        self.cfg_items = A2List(edit)
        self.cfg_items.setMaximumSize(QtCore.QSize(16777215, 145))
        self.cfg_items.setAlternatingRowColors(True)
        self.cfg_items.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.cfg_items.setObjectName("cfg_items")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_items)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(edit)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(40, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plus_button = QtWidgets.QPushButton(edit)
        self.plus_button.setMaximumSize(QtCore.QSize(50, 50))
        self.plus_button.setObjectName("plus_button")
        self.verticalLayout_2.addWidget(self.plus_button)
        self.minus_button = QtWidgets.QPushButton(edit)
        self.minus_button.setMaximumSize(QtCore.QSize(50, 50))
        self.minus_button.setAutoDefault(True)
        self.minus_button.setObjectName("minus_button")
        self.verticalLayout_2.addWidget(self.minus_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.edit_layout.setLayout(2, QtWidgets.QFormLayout.LabelRole, self.verticalLayout)
        self.cfg_user_edit = QtWidgets.QCheckBox(edit)
        self.cfg_user_edit.setObjectName("cfg_user_edit")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_user_edit)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.internalNameLabel.setText(QtWidgets.QApplication.translate("edit", "internal name:", None, -1))
        self.cfg_name.setText(QtWidgets.QApplication.translate("edit", "extensionX_combobox1", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "display label:", None, -1))
        self.cfg_label.setText(QtWidgets.QApplication.translate("edit", "some values", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("edit", "items:", None, -1))
        self.plus_button.setText(QtWidgets.QApplication.translate("edit", "+", None, -1))
        self.minus_button.setText(QtWidgets.QApplication.translate("edit", "-", None, -1))
        self.cfg_user_edit.setText(QtWidgets.QApplication.translate("edit", "allow user edit", None, -1))

from a2widget.a2list import A2List
