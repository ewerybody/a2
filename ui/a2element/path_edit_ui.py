# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\path_edit.ui'
#
# Created: Mon Mar 13 14:54:24 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(488, 240)
        self.edit_layout = QtGui.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setContentsMargins(10, 5, 0, 5)
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
        self.cfg_value = A2PathField(edit)
        self.cfg_value.setText("")
        self.cfg_value.setObjectName("cfg_value")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_value)
        self.defaultPathLabel = QtGui.QLabel(edit)
        self.defaultPathLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.defaultPathLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.defaultPathLabel.setObjectName("defaultPathLabel")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.defaultPathLabel)
        self.cfg_writable = QtGui.QCheckBox(edit)
        self.cfg_writable.setObjectName("cfg_writable")
        self.edit_layout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cfg_writable)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cfg_browse_type_0 = QtGui.QRadioButton(edit)
        self.cfg_browse_type_0.setObjectName("cfg_browse_type_0")
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_0)
        self.cfg_browse_type_1 = QtGui.QRadioButton(edit)
        self.cfg_browse_type_1.setChecked(True)
        self.cfg_browse_type_1.setObjectName("cfg_browse_type_1")
        self.horizontalLayout_2.addWidget(self.cfg_browse_type_1)
        self.cfg_save_mode = QtGui.QCheckBox(edit)
        self.cfg_save_mode.setObjectName("cfg_save_mode")
        self.horizontalLayout_2.addWidget(self.cfg_save_mode)
        self.horizontalLayout_2.setStretch(2, 1)
        self.edit_layout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_3 = QtGui.QLabel(edit)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(edit)
        self.label_4.setEnabled(True)
        self.label_4.setMinimumSize(QtCore.QSize(100, 0))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.edit_layout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_4)
        self.cfg_file_types = QtGui.QLineEdit(edit)
        self.cfg_file_types.setText("")
        self.cfg_file_types.setObjectName("cfg_file_types")
        self.edit_layout.setWidget(5, QtGui.QFormLayout.FieldRole, self.cfg_file_types)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("edit", "extensionX_path1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("edit", "some path bla", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultPathLabel.setText(QtGui.QApplication.translate("edit", "default path:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_writable.setText(QtGui.QApplication.translate("edit", "writable field", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_browse_type_0.setText(QtGui.QApplication.translate("edit", "folder", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_browse_type_1.setText(QtGui.QApplication.translate("edit", "file", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_save_mode.setText(QtGui.QApplication.translate("edit", "save mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("edit", "browse mode:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("edit", "file types:", None, QtGui.QApplication.UnicodeUTF8))

from a2widget import A2PathField
