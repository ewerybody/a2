# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\button_edit.ui'
#
# Created: Mon Nov 14 14:37:15 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(607, 296)
        self.edit_layout = QtGui.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setObjectName("edit_layout")
        self.displayLabelLabel = QtGui.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_labeltext = QtGui.QLineEdit(edit)
        self.cfg_labeltext.setText("")
        self.cfg_labeltext.setPlaceholderText("space used by button if no label text")
        self.cfg_labeltext.setObjectName("cfg_labeltext")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cfg_labeltext)
        self.displayLabelLabel_2 = QtGui.QLabel(edit)
        self.displayLabelLabel_2.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_2.setObjectName("displayLabelLabel_2")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.displayLabelLabel_2)
        self.cfg_buttontext = QtGui.QLineEdit(edit)
        self.cfg_buttontext.setText("")
        self.cfg_buttontext.setObjectName("cfg_buttontext")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cfg_buttontext)
        self.displayLabelLabel_3 = QtGui.QLabel(edit)
        self.displayLabelLabel_3.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel_3.setObjectName("displayLabelLabel_3")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.displayLabelLabel_3)
        self.cfg_code = A2CodeField(edit)
        self.cfg_code.setObjectName("cfg_code")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_code)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "label text:", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel_2.setText(QtGui.QApplication.translate("edit", "button text:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_buttontext.setPlaceholderText(QtGui.QApplication.translate("edit", "text to show on the button", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel_3.setText(QtGui.QApplication.translate("edit", "Python Code:", None, QtGui.QApplication.UnicodeUTF8))

from a2widget import A2CodeField
