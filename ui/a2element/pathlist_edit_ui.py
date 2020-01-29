# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2element\pathlist_edit.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2element\pathlist_edit.ui' applies.
#
# Created: Tue Jan 28 21:59:37 2020
#      by: pyside2-uic  running on PySide2 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(549, 124)
        self.edit_layout = QtWidgets.QFormLayout(edit)
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
        self.cfg_max_items = QtWidgets.QSpinBox(edit)
        self.cfg_max_items.setSuffix("")
        self.cfg_max_items.setPrefix("")
        self.cfg_max_items.setMinimum(1)
        self.cfg_max_items.setMaximum(99)
        self.cfg_max_items.setObjectName("cfg_max_items")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_max_items)
        self.maxItemsLabel = QtWidgets.QLabel(edit)
        self.maxItemsLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.maxItemsLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxItemsLabel.setObjectName("maxItemsLabel")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.maxItemsLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cfg_browse_type_0 = QtWidgets.QRadioButton(edit)
        self.cfg_browse_type_0.setChecked(True)
        self.cfg_browse_type_0.setObjectName("cfg_browse_type_0")
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_0)
        self.cfg_browse_type_1 = QtWidgets.QRadioButton(edit)
        self.cfg_browse_type_1.setObjectName("cfg_browse_type_1")
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.edit_layout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_3 = QtWidgets.QLabel(edit)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.internalNameLabel.setText(QtWidgets.QApplication.translate("edit", "internal name:", None, -1))
        self.cfg_name.setText(QtWidgets.QApplication.translate("edit", "extensionX_path1", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "display label:", None, -1))
        self.cfg_label.setText(QtWidgets.QApplication.translate("edit", "some pathlist bla", None, -1))
        self.maxItemsLabel.setText(QtWidgets.QApplication.translate("edit", "max items:", None, -1))
        self.cfg_browse_type_0.setText(QtWidgets.QApplication.translate("edit", "folder", None, -1))
        self.cfg_browse_type_1.setText(QtWidgets.QApplication.translate("edit", "file", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("edit", "type:", None, -1))

