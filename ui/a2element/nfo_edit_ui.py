# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2element\nfo_edit.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2element\nfo_edit.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(1059, 579)
        self.edit_layout = QtWidgets.QFormLayout(edit)
        self.edit_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.edit_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edit_layout.setObjectName("edit_layout")
        self.cfg_description = QtWidgets.QTextEdit(edit)
        self.cfg_description.setMaximumSize(QtCore.QSize(16777215, 100))
        self.cfg_description.setObjectName("cfg_description")
        self.edit_layout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.cfg_description)
        self.internalNameLabel = QtWidgets.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_author = QtWidgets.QLineEdit(edit)
        self.cfg_author.setText("")
        self.cfg_author.setObjectName("cfg_author")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_author)
        self.displayLabelLabel = QtWidgets.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_version = QtWidgets.QLineEdit(edit)
        self.cfg_version.setText("")
        self.cfg_version.setObjectName("cfg_version")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_version)
        self.label = QtWidgets.QLabel(edit)
        self.label.setObjectName("label")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cfg_date = QtWidgets.QLineEdit(edit)
        self.cfg_date.setText("")
        self.cfg_date.setObjectName("cfg_date")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_date)
        self.label_2 = QtWidgets.QLabel(edit)
        self.label_2.setObjectName("label_2")
        self.edit_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cfg_url = QtWidgets.QLineEdit(edit)
        self.cfg_url.setText("")
        self.cfg_url.setObjectName("cfg_url")
        self.edit_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cfg_url)
        self.label_3 = QtWidgets.QLabel(edit)
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cfg_tags = A2TagField(edit)
        self.cfg_tags.setObjectName("cfg_tags")
        self.edit_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.cfg_tags)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtWidgets.QApplication.translate("edit", "Form", None, -1))
        self.internalNameLabel.setText(QtWidgets.QApplication.translate("edit", "Author:", None, -1))
        self.displayLabelLabel.setText(QtWidgets.QApplication.translate("edit", "Version:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("edit", "Date:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("edit", "URL:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("edit", "Tags:", None, -1))

from a2widget import A2TagField
