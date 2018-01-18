# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\pathlist_edit.ui'
#
# Created: Thu Jan 18 16:30:54 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(549, 124)
        self.edit_layout = QtGui.QFormLayout(edit)
        self.edit_layout.setObjectName("edit_layout")
        self.internalNameLabel = QtGui.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_name = QtGui.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cfg_name)
        self.displayLabelLabel = QtGui.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_label = QtGui.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cfg_label)
        self.cfg_max_items = QtGui.QSpinBox(edit)
        self.cfg_max_items.setSuffix("")
        self.cfg_max_items.setPrefix("")
        self.cfg_max_items.setMinimum(1)
        self.cfg_max_items.setMaximum(99)
        self.cfg_max_items.setObjectName("cfg_max_items")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_max_items)
        self.maxItemsLabel = QtGui.QLabel(edit)
        self.maxItemsLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.maxItemsLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxItemsLabel.setObjectName("maxItemsLabel")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.maxItemsLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cfg_browse_type_0 = QtGui.QRadioButton(edit)
        self.cfg_browse_type_0.setChecked(True)
        self.cfg_browse_type_0.setObjectName("cfg_browse_type_0")
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_0)
        self.cfg_browse_type_1 = QtGui.QRadioButton(edit)
        self.cfg_browse_type_1.setObjectName("cfg_browse_type_1")
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.edit_layout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_3 = QtGui.QLabel(edit)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("edit", "extensionX_path1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("edit", "some pathlist bla", None, QtGui.QApplication.UnicodeUTF8))
        self.maxItemsLabel.setText(QtGui.QApplication.translate("edit", "max items:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_browse_type_0.setText(QtGui.QApplication.translate("edit", "folder", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_browse_type_1.setText(QtGui.QApplication.translate("edit", "file", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("edit", "type:", None, QtGui.QApplication.UnicodeUTF8))

