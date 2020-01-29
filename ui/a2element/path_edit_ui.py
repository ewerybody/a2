# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2element\path_edit.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2element\path_edit.ui' applies.
#
# Created: Tue Jan 28 21:59:37 2020
#      by: pyside2-uic  running on PySide2 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(488, 240)
        self.edit_layout = QtWidgets.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setContentsMargins(10, 5, 0, 5)
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
        self.cfg_value = A2PathField(edit)
        self.cfg_value.setText("")
        self.cfg_value.setObjectName("cfg_value")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_value)
        self.defaultPathLabel = QtWidgets.QLabel(edit)
        self.defaultPathLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.defaultPathLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.defaultPathLabel.setObjectName("defaultPathLabel")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.defaultPathLabel)
        self.cfg_writable = QtWidgets.QCheckBox(edit)
        self.cfg_writable.setObjectName("cfg_writable")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_writable)
        self.browse_type_layout = QtWidgets.QHBoxLayout()
        self.browse_type_layout.setObjectName("browse_type_layout")
        self.cfg_browse_type_0 = QtWidgets.QRadioButton(edit)
        self.cfg_browse_type_0.setObjectName("cfg_browse_type_0")
        self.browse_type_layout.addWidget(self.cfg_browse_type_0)
        self.cfg_browse_type_1 = QtWidgets.QRadioButton(edit)
        self.cfg_browse_type_1.setChecked(True)
        self.cfg_browse_type_1.setObjectName("cfg_browse_type_1")
        self.browse_type_layout.addWidget(self.cfg_browse_type_1)
        self.cfg_save_mode = QtWidgets.QCheckBox(edit)
        self.cfg_save_mode.setObjectName("cfg_save_mode")
        self.browse_type_layout.addWidget(self.cfg_save_mode)
        self.edit_layout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.browse_type_layout)
        self.label_3 = QtWidgets.QLabel(edit)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.file_types_label = QtWidgets.QLabel(edit)
        self.file_types_label.setEnabled(True)
        self.file_types_label.setMinimumSize(QtCore.QSize(100, 0))
        self.file_types_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.file_types_label.setObjectName("file_types_label")
        self.edit_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.file_types_label)
        self.cfg_file_types = QtWidgets.QLineEdit(edit)
        self.cfg_file_types.setText("")
        self.cfg_file_types.setObjectName("cfg_file_types")
        self.edit_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.cfg_file_types)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.internalNameLabel.setText(QtWidgets.QApplication.translate("edit", "internal name:", None, -1))
        self.cfg_name.setText(QtWidgets.QApplication.translate("edit", "extensionX_path1", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "display label:", None, -1))
        self.cfg_label.setText(QtWidgets.QApplication.translate("edit", "some path bla", None, -1))
        self.defaultPathLabel.setText(QtWidgets.QApplication.translate("edit", "default path:", None, -1))
        self.cfg_writable.setText(QtWidgets.QApplication.translate("edit", "writable field", None, -1))
        self.cfg_browse_type_0.setText(QtWidgets.QApplication.translate("edit", "folder", None, -1))
        self.cfg_browse_type_1.setText(QtWidgets.QApplication.translate("edit", "file", None, -1))
        self.cfg_save_mode.setText(QtWidgets.QApplication.translate("edit", "save mode", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("edit", "browse mode:", None, -1))
        self.file_types_label.setText(QtWidgets.QApplication.translate("edit", "file types:", None, -1))

from a2widget.a2path_field import A2PathField
