# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file:
#   'a2\ui\a2element\nfo_edit.ui'
# licensing of that file applies.
#
# Created: Tue Sep 29 17:15:13 2020
#      by: pyside2-uic  running on PySide2 5.15.1
#
# pylint: disable=W0201,C0103,C0111
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_edit:
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(1059, 287)
        edit.setWindowTitle("Form")
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
        self.internalNameLabel.setText("Author:")
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.internalNameLabel)
        self.cfg_author = QtWidgets.QLineEdit(edit)
        self.cfg_author.setObjectName("cfg_author")
        self.edit_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cfg_author)
        self.displayLabelLabel = QtWidgets.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setText("Version:")
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.displayLabelLabel)
        self.cfg_version = QtWidgets.QLineEdit(edit)
        self.cfg_version.setObjectName("cfg_version")
        self.edit_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cfg_version)
        self.label = QtWidgets.QLabel(edit)
        self.label.setText("Date:")
        self.label.setObjectName("label")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cfg_date = QtWidgets.QLineEdit(edit)
        self.cfg_date.setObjectName("cfg_date")
        self.edit_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cfg_date)
        self.label_2 = QtWidgets.QLabel(edit)
        self.label_2.setText("URL:")
        self.label_2.setObjectName("label_2")
        self.edit_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cfg_url = QtWidgets.QLineEdit(edit)
        self.cfg_url.setObjectName("cfg_url")
        self.edit_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cfg_url)
        self.label_3 = QtWidgets.QLabel(edit)
        self.label_3.setText("Tags:")
        self.label_3.setObjectName("label_3")
        self.edit_layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cfg_tags = A2TagField(edit)
        self.cfg_tags.setObjectName("cfg_tags")
        self.edit_layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.cfg_tags)
        QtCore.QMetaObject.connectSlotsByName(edit)

from a2widget.a2tag_field import A2TagField
