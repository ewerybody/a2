# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\number_edit.ui'
#
# Created: Mon Mar 13 14:52:05 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(468, 234)
        self.edit_layout = QtGui.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
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
        self.label = QtGui.QLabel(edit)
        self.label.setObjectName("label")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.value = QtGui.QDoubleSpinBox(edit)
        self.value.setSuffix("")
        self.value.setDecimals(0)
        self.value.setSingleStep(1.0)
        self.value.setProperty("value", 0.0)
        self.value.setObjectName("value")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.value)
        self.label_2 = QtGui.QLabel(edit)
        self.label_2.setObjectName("label_2")
        self.edit_layout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cfg_min = QtGui.QDoubleSpinBox(edit)
        self.cfg_min.setMinimum(-16777215.0)
        self.cfg_min.setProperty("value", 0.0)
        self.cfg_min.setObjectName("cfg_min")
        self.horizontalLayout.addWidget(self.cfg_min)
        self.cfg_max = QtGui.QDoubleSpinBox(edit)
        self.cfg_max.setMinimum(-16777215.0)
        self.cfg_max.setMaximum(16777215.0)
        self.cfg_max.setProperty("value", 100.0)
        self.cfg_max.setObjectName("cfg_max")
        self.horizontalLayout.addWidget(self.cfg_max)
        self.edit_layout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_3 = QtGui.QLabel(edit)
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cfg_decimals = QtGui.QSpinBox(edit)
        self.cfg_decimals.setProperty("value", 1)
        self.cfg_decimals.setObjectName("cfg_decimals")
        self.edit_layout.setWidget(4, QtGui.QFormLayout.FieldRole, self.cfg_decimals)
        self.label_4 = QtGui.QLabel(edit)
        self.label_4.setObjectName("label_4")
        self.edit_layout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_4)
        self.cfg_step_len = QtGui.QDoubleSpinBox(edit)
        self.cfg_step_len.setMaximum(16777215.0)
        self.cfg_step_len.setProperty("value", 1.0)
        self.cfg_step_len.setObjectName("cfg_step_len")
        self.edit_layout.setWidget(5, QtGui.QFormLayout.FieldRole, self.cfg_step_len)
        self.label_5 = QtGui.QLabel(edit)
        self.label_5.setObjectName("label_5")
        self.edit_layout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_5)
        self.cfg_suffix = QtGui.QLineEdit(edit)
        self.cfg_suffix.setObjectName("cfg_suffix")
        self.edit_layout.setWidget(6, QtGui.QFormLayout.FieldRole, self.cfg_suffix)
        self.cfg_slider = QtGui.QCheckBox(edit)
        self.cfg_slider.setObjectName("cfg_slider")
        self.edit_layout.setWidget(7, QtGui.QFormLayout.FieldRole, self.cfg_slider)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("edit", "extensionX_number1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("edit", "some number", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("edit", "default value:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("edit", "min/max:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("edit", "decimals:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("edit", "step length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("edit", "suffix label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_slider.setText(QtGui.QApplication.translate("edit", "show slider", None, QtGui.QApplication.UnicodeUTF8))

