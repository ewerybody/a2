# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2ctrl\group_edit.ui'
#
# Created: Fri Apr  1 02:07:48 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_edit(object):
    def setupUi(self, edit):
        edit.setObjectName("edit")
        edit.resize(1082, 306)
        self.groupLayout = QtGui.QVBoxLayout(edit)
        self.groupLayout.setSpacing(5)
        self.groupLayout.setContentsMargins(10, 5, 0, 5)
        self.groupLayout.setObjectName("groupLayout")
        self.internalNameLayout = QtGui.QHBoxLayout()
        self.internalNameLayout.setSpacing(10)
        self.internalNameLayout.setObjectName("internalNameLayout")
        self.internalNameLabel = QtGui.QLabel(edit)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.internalNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.internalNameLayout.addWidget(self.internalNameLabel)
        self.cfg_name = QtGui.QLineEdit(edit)
        self.cfg_name.setObjectName("cfg_name")
        self.internalNameLayout.addWidget(self.cfg_name)
        self.groupLayout.addLayout(self.internalNameLayout)
        self.displayLabelLayout = QtGui.QHBoxLayout()
        self.displayLabelLayout.setSpacing(10)
        self.displayLabelLayout.setObjectName("displayLabelLayout")
        self.displayLabelLabel = QtGui.QLabel(edit)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.displayLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.displayLabelLayout.addWidget(self.displayLabelLabel)
        self.cfg_label = QtGui.QLineEdit(edit)
        self.cfg_label.setObjectName("cfg_label")
        self.displayLabelLayout.addWidget(self.cfg_label)
        self.groupLayout.addLayout(self.displayLabelLayout)
        self.enabledLayout = QtGui.QHBoxLayout()
        self.enabledLayout.setSpacing(10)
        self.enabledLayout.setObjectName("enabledLayout")
        self.label = QtGui.QLabel(edit)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setText("")
        self.label.setObjectName("label")
        self.enabledLayout.addWidget(self.label)
        self.cfg_disablable = QtGui.QCheckBox(edit)
        self.cfg_disablable.setChecked(True)
        self.cfg_disablable.setObjectName("cfg_disablable")
        self.enabledLayout.addWidget(self.cfg_disablable)
        self.enabledLayout.setStretch(1, 1)
        self.groupLayout.addLayout(self.enabledLayout)
        self.enabledLayout_2 = QtGui.QHBoxLayout()
        self.enabledLayout_2.setSpacing(10)
        self.enabledLayout_2.setContentsMargins(-1, -1, -1, 10)
        self.enabledLayout_2.setObjectName("enabledLayout_2")
        self.label_2 = QtGui.QLabel(edit)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.enabledLayout_2.addWidget(self.label_2)
        self.cfg_enabled = QtGui.QCheckBox(edit)
        self.cfg_enabled.setChecked(True)
        self.cfg_enabled.setObjectName("cfg_enabled")
        self.enabledLayout_2.addWidget(self.cfg_enabled)
        self.enabledLayout_2.setStretch(1, 1)
        self.groupLayout.addLayout(self.enabledLayout_2)

        self.retranslateUi(edit)
        QtCore.QMetaObject.connectSlotsByName(edit)

    def retranslateUi(self, edit):
        edit.setWindowTitle(QtGui.QApplication.translate("edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("edit", "extensionX_group1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("edit", "some group name", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_disablable.setText(QtGui.QApplication.translate("edit", "disablable", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_enabled.setText(QtGui.QApplication.translate("edit", "enabled by default", None, QtGui.QApplication.UnicodeUTF8))

