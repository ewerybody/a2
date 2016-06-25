# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2ctrl\combo_edit.ui'
#
# Created: Sat Jun 25 18:42:50 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(837, 499)
        self.editLayout = QtGui.QFormLayout(edit)
        self.editLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.editLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.editLayout.setObjectName("editLayout")
        self.internalNameLabel = QtGui.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.editLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtGui.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.editLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QtGui.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.editLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtGui.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.editLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cfg_label)
        self.cfg_items = QtGui.QListWidget(edit)
        self.cfg_items.setMaximumSize(QtCore.QSize(16777215, 145))
        self.cfg_items.setAlternatingRowColors(True)
        self.cfg_items.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.cfg_items.setObjectName("cfg_items")
        self.editLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_items)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtGui.QLabel(edit)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(40, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plus_button = QtGui.QPushButton(edit)
        self.plus_button.setMaximumSize(QtCore.QSize(50, 50))
        self.plus_button.setObjectName("plus_button")
        self.verticalLayout_2.addWidget(self.plus_button)
        self.minus_button = QtGui.QPushButton(edit)
        self.minus_button.setMaximumSize(QtCore.QSize(50, 50))
        self.minus_button.setAutoDefault(True)
        self.minus_button.setObjectName("minus_button")
        self.verticalLayout_2.addWidget(self.minus_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.editLayout.setLayout(2, QtGui.QFormLayout.LabelRole, self.verticalLayout)
        self.cfg_user_edit = QtGui.QCheckBox(edit)
        self.cfg_user_edit.setObjectName("cfg_user_edit")
        self.editLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cfg_user_edit)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("edit", "extensionX_combobox1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("edit", "some values", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("edit", "items:", None, QtGui.QApplication.UnicodeUTF8))
        self.plus_button.setText(QtGui.QApplication.translate("edit", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.minus_button.setText(QtGui.QApplication.translate("edit", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_user_edit.setText(QtGui.QApplication.translate("edit", "allow user edit", None, QtGui.QApplication.UnicodeUTF8))

