# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2element\nfo_edit.ui'
#
# Created: Mon Sep 12 23:50:01 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(737, 356)
        self.edit_layout = QtGui.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setObjectName("edit_layout")
        self.cfg_description = QtGui.QTextEdit(edit)
        self.cfg_description.setObjectName("cfg_description")
        self.edit_layout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.cfg_description)
        self.internalNameLabel = QtGui.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_author = QtGui.QLineEdit(edit)
        self.cfg_author.setText("")
        self.cfg_author.setObjectName("cfg_author")
        self.edit_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cfg_author)
        self.displayLabelLabel = QtGui.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_version = QtGui.QLineEdit(edit)
        self.cfg_version.setText("")
        self.cfg_version.setObjectName("cfg_version")
        self.edit_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cfg_version)
        self.label = QtGui.QLabel(edit)
        self.label.setObjectName("label")
        self.edit_layout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label)
        self.cfg_date = QtGui.QLineEdit(edit)
        self.cfg_date.setText("")
        self.cfg_date.setObjectName("cfg_date")
        self.edit_layout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cfg_date)
        self.label_2 = QtGui.QLabel(edit)
        self.label_2.setObjectName("label_2")
        self.edit_layout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.cfg_url = QtGui.QLineEdit(edit)
        self.cfg_url.setText("")
        self.cfg_url.setObjectName("cfg_url")
        self.edit_layout.setWidget(4, QtGui.QFormLayout.FieldRole, self.cfg_url)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "Author:", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("edit", "Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("edit", "URL:", None, QtGui.QApplication.UnicodeUTF8))

