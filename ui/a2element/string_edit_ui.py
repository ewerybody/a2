# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2element\string_edit.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2element\string_edit.ui' applies.
#
# Created: Tue Jan 28 21:59:37 2020
#      by: pyside2-uic  running on PySide2 5.14.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(495, 239)
        self.formLayout = QtWidgets.QFormLayout(edit)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(edit)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cfg_name = QtWidgets.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cfg_name)
        self.label_2 = QtWidgets.QLabel(edit)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cfg_label = QtWidgets.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_label)
        self.cfg_label_over_field = QtWidgets.QCheckBox(edit)
        self.cfg_label_over_field.setObjectName("cfg_label_over_field")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_label_over_field)
        self.label_3 = QtWidgets.QLabel(edit)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cfg_value = A2TextField(edit)
        self.cfg_value.setObjectName("cfg_value")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_value)
        self.cfg_password_mode = QtWidgets.QCheckBox(edit)
        self.cfg_password_mode.setText("password mode (forces single line)")
        self.cfg_password_mode.setObjectName("cfg_password_mode")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cfg_password_mode)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("edit", "internal name:", None, -1))
        self.cfg_name.setText(QtWidgets.QApplication.translate("edit", "extensionX_string1", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("edit", "display label:", None, -1))
        self.cfg_label.setText(QtWidgets.QApplication.translate("edit", "some string bla", None, -1))
        self.cfg_label_over_field.setText(QtWidgets.QApplication.translate("edit", "Label over field", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("edit", "default text:", None, -1))

from a2widget.a2text_field import A2TextField
