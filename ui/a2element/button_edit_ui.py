# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\button_edit.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2element\button_edit.ui' applies.
#
# Created: Wed Nov 21 20:45:50 2018
#      by: pyside2-uic  running on PySide2 5.11.1a1.dev1542405709
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(607, 195)
        self.edit_layout = QtWidgets.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setObjectName("edit_layout")
        self.displayLabelLabel = QtWidgets.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_labeltext = QtWidgets.QLineEdit(edit)
        self.cfg_labeltext.setText("")
        self.cfg_labeltext.setPlaceholderText("Space used by Button if empty!")
        self.cfg_labeltext.setObjectName("cfg_labeltext")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cfg_labeltext)
        self.displayLabelLabel_2 = QtWidgets.QLabel(edit)
        self.displayLabelLabel_2.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_2.setObjectName("displayLabelLabel_2")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel_2)
        self.cfg_buttontext = QtWidgets.QLineEdit(edit)
        self.cfg_buttontext.setText("")
        self.cfg_buttontext.setObjectName("cfg_buttontext")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_buttontext)
        self.displayLabelLabel_3 = QtWidgets.QLabel(edit)
        self.displayLabelLabel_3.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_3.setObjectName("displayLabelLabel_3")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel_3)
        self.script_selector = ScriptSelector(edit)
        self.script_selector.setObjectName("script_selector")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.script_selector)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "label text", None, -1))
        self.displayLabelLabel_2.setText(QtWidgets.QApplication.translate("edit", "button text", None, -1))
        self.cfg_buttontext.setPlaceholderText(QtWidgets.QApplication.translate("edit", "Text to show on the Button.", None, -1))
        self.displayLabelLabel_3.setText(QtWidgets.QApplication.translate("edit", "python script", None, -1))

from a2widget.local_script import ScriptSelector
