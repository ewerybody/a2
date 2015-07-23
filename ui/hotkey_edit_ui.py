# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hotkey_edit.ui'
#
# Created: Thu Jul 23 12:16:39 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_hotkey_edit(object):
    def setupUi(self, hotkey_edit):
        hotkey_edit.setObjectName("hotkey_edit")
        hotkey_edit.resize(574, 384)
        self.hotkeyCtrlLayout = QtGui.QVBoxLayout(hotkey_edit)
        self.hotkeyCtrlLayout.setSpacing(0)
        self.hotkeyCtrlLayout.setContentsMargins(0, 0, 0, 0)
        self.hotkeyCtrlLayout.setObjectName("hotkeyCtrlLayout")
        self.groupBox = QtGui.QGroupBox(hotkey_edit)
        self.groupBox.setStyleSheet("QGroupBox {font: 10pt};")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setContentsMargins(15, 5, 15, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.internalNameLayout = QtGui.QHBoxLayout()
        self.internalNameLayout.setObjectName("internalNameLayout")
        self.internalNameLabel = QtGui.QLabel(self.groupBox)
        self.internalNameLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.internalNameLabel.setObjectName("internalNameLabel")
        self.internalNameLayout.addWidget(self.internalNameLabel)
        self.cfg_name = QtGui.QLineEdit(self.groupBox)
        self.cfg_name.setObjectName("cfg_name")
        self.internalNameLayout.addWidget(self.cfg_name)
        self.verticalLayout_2.addLayout(self.internalNameLayout)
        self.displayLabelLayout = QtGui.QHBoxLayout()
        self.displayLabelLayout.setObjectName("displayLabelLayout")
        self.displayLabelLabel = QtGui.QLabel(self.groupBox)
        self.displayLabelLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.displayLabelLabel.setObjectName("displayLabelLabel")
        self.displayLabelLayout.addWidget(self.displayLabelLabel)
        self.cfg_label = QtGui.QLineEdit(self.groupBox)
        self.cfg_label.setObjectName("cfg_label")
        self.displayLabelLayout.addWidget(self.cfg_label)
        self.verticalLayout_2.addLayout(self.displayLabelLayout)
        self.hotkeyLayout = QtGui.QHBoxLayout()
        self.hotkeyLayout.setContentsMargins(-1, -1, -1, 10)
        self.hotkeyLayout.setObjectName("hotkeyLayout")
        self.hotkeyLabelLayout = QtGui.QVBoxLayout()
        self.hotkeyLabelLayout.setObjectName("hotkeyLabelLayout")
        self.hotkeyLabel = QtGui.QLabel(self.groupBox)
        self.hotkeyLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.hotkeyLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        self.hotkeyLabel.setObjectName("hotkeyLabel")
        self.hotkeyLabelLayout.addWidget(self.hotkeyLabel)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.hotkeyLabelLayout.addItem(spacerItem)
        self.hotkeyLayout.addLayout(self.hotkeyLabelLayout)
        self.hotkeyKeyLayout = QtGui.QVBoxLayout()
        self.hotkeyKeyLayout.setSpacing(5)
        self.hotkeyKeyLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.hotkeyKeyLayout.setObjectName("hotkeyKeyLayout")
        self.cfg_enabled = QtGui.QCheckBox(self.groupBox)
        self.cfg_enabled.setChecked(True)
        self.cfg_enabled.setObjectName("cfg_enabled")
        self.hotkeyKeyLayout.addWidget(self.cfg_enabled)
        self.cfg_disablable = QtGui.QCheckBox(self.groupBox)
        self.cfg_disablable.setChecked(True)
        self.cfg_disablable.setObjectName("cfg_disablable")
        self.hotkeyKeyLayout.addWidget(self.cfg_disablable)
        self.cfg_keyChange = QtGui.QCheckBox(self.groupBox)
        self.cfg_keyChange.setChecked(True)
        self.cfg_keyChange.setObjectName("cfg_keyChange")
        self.hotkeyKeyLayout.addWidget(self.cfg_keyChange)
        self.cfg_multiple = QtGui.QCheckBox(self.groupBox)
        self.cfg_multiple.setChecked(True)
        self.cfg_multiple.setObjectName("cfg_multiple")
        self.hotkeyKeyLayout.addWidget(self.cfg_multiple)
        self.hotkeyLayout.addLayout(self.hotkeyKeyLayout)
        self.hotkeyLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.hotkeyLayout)
        self.functionLayout = QtGui.QHBoxLayout()
        self.functionLayout.setContentsMargins(-1, -1, -1, 10)
        self.functionLayout.setObjectName("functionLayout")
        self.functionLabelLayout = QtGui.QVBoxLayout()
        self.functionLabelLayout.setObjectName("functionLabelLayout")
        self.functionLabel = QtGui.QLabel(self.groupBox)
        self.functionLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.functionLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        self.functionLabel.setObjectName("functionLabel")
        self.functionLabelLayout.addWidget(self.functionLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.functionLabelLayout.addItem(spacerItem1)
        self.functionLayout.addLayout(self.functionLabelLayout)
        self.functionCtrlLayout = QtGui.QVBoxLayout()
        self.functionCtrlLayout.setSpacing(6)
        self.functionCtrlLayout.setContentsMargins(-1, -1, -1, 0)
        self.functionCtrlLayout.setObjectName("functionCtrlLayout")
        self.functionRowLayout = QtGui.QHBoxLayout()
        self.functionRowLayout.setContentsMargins(-1, 0, -1, -1)
        self.functionRowLayout.setObjectName("functionRowLayout")
        self.cfg_functionMode = QtGui.QComboBox(self.groupBox)
        self.cfg_functionMode.setObjectName("cfg_functionMode")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.cfg_functionMode.addItem("")
        self.functionRowLayout.addWidget(self.cfg_functionMode)
        self.functionButton = QtGui.QPushButton(self.groupBox)
        self.functionButton.setMaximumSize(QtCore.QSize(50, 35))
        self.functionButton.setObjectName("functionButton")
        self.functionRowLayout.addWidget(self.functionButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.functionRowLayout.addItem(spacerItem2)
        self.functionCtrlLayout.addLayout(self.functionRowLayout)
        self.functionText = QtGui.QLineEdit(self.groupBox)
        self.functionText.setObjectName("functionText")
        self.functionCtrlLayout.addWidget(self.functionText)
        self.functionLayout.addLayout(self.functionCtrlLayout)
        self.functionLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.functionLayout)
        self.scopeLayout = QtGui.QHBoxLayout()
        self.scopeLayout.setContentsMargins(-1, -1, -1, 10)
        self.scopeLayout.setObjectName("scopeLayout")
        self.scopeLabelLayout = QtGui.QVBoxLayout()
        self.scopeLabelLayout.setObjectName("scopeLabelLayout")
        self.scopeLabel = QtGui.QLabel(self.groupBox)
        self.scopeLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.scopeLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        self.scopeLabel.setObjectName("scopeLabel")
        self.scopeLabelLayout.addWidget(self.scopeLabel)
        spacerItem3 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.scopeLabelLayout.addItem(spacerItem3)
        self.scopeLayout.addLayout(self.scopeLabelLayout)
        self.scopeCtrlLayout = QtGui.QVBoxLayout()
        self.scopeCtrlLayout.setSpacing(5)
        self.scopeCtrlLayout.setContentsMargins(-1, -1, -1, 0)
        self.scopeCtrlLayout.setObjectName("scopeCtrlLayout")
        self.scopeRowLayout = QtGui.QHBoxLayout()
        self.scopeRowLayout.setContentsMargins(-1, 0, -1, -1)
        self.scopeRowLayout.setObjectName("scopeRowLayout")
        self.cfg_scopeMode = QtGui.QComboBox(self.groupBox)
        self.cfg_scopeMode.setObjectName("cfg_scopeMode")
        self.cfg_scopeMode.addItem("")
        self.cfg_scopeMode.addItem("")
        self.cfg_scopeMode.addItem("")
        self.scopeRowLayout.addWidget(self.cfg_scopeMode)
        self.scopePlus = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopePlus.sizePolicy().hasHeightForWidth())
        self.scopePlus.setSizePolicy(sizePolicy)
        self.scopePlus.setMaximumSize(QtCore.QSize(50, 35))
        self.scopePlus.setObjectName("scopePlus")
        self.scopeRowLayout.addWidget(self.scopePlus)
        self.scopeMinus = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeMinus.sizePolicy().hasHeightForWidth())
        self.scopeMinus.setSizePolicy(sizePolicy)
        self.scopeMinus.setMaximumSize(QtCore.QSize(50, 35))
        self.scopeMinus.setObjectName("scopeMinus")
        self.scopeRowLayout.addWidget(self.scopeMinus)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.scopeRowLayout.addItem(spacerItem4)
        self.scopeCtrlLayout.addLayout(self.scopeRowLayout)
        self.cfg_scope = QtGui.QListWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfg_scope.sizePolicy().hasHeightForWidth())
        self.cfg_scope.setSizePolicy(sizePolicy)
        self.cfg_scope.setMaximumSize(QtCore.QSize(16777215, 75))
        self.cfg_scope.setObjectName("cfg_scope")
        self.scopeCtrlLayout.addWidget(self.cfg_scope)
        self.cfg_scopeChange = QtGui.QCheckBox(self.groupBox)
        self.cfg_scopeChange.setChecked(True)
        self.cfg_scopeChange.setObjectName("cfg_scopeChange")
        self.scopeCtrlLayout.addWidget(self.cfg_scopeChange)
        self.scopeLayout.addLayout(self.scopeCtrlLayout)
        self.scopeLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.scopeLayout)
        self.hotkeyCtrlLayout.addWidget(self.groupBox)

        self.retranslateUi(hotkey_edit)
        QtCore.QMetaObject.connectSlotsByName(hotkey_edit)

    def retranslateUi(self, hotkey_edit):
        hotkey_edit.setWindowTitle(QtGui.QApplication.translate("hotkey_edit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("hotkey_edit", "hotkey", None, QtGui.QApplication.UnicodeUTF8))
        self.internalNameLabel.setText(QtGui.QApplication.translate("hotkey_edit", "internal name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_name.setText(QtGui.QApplication.translate("hotkey_edit", "extensionXhotkey1", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLabelLabel.setText(QtGui.QApplication.translate("hotkey_edit", "display label:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_label.setText(QtGui.QApplication.translate("hotkey_edit", "make some awesome stuff", None, QtGui.QApplication.UnicodeUTF8))
        self.hotkeyLabel.setText(QtGui.QApplication.translate("hotkey_edit", "hotkey:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_enabled.setText(QtGui.QApplication.translate("hotkey_edit", "enabled by default", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_disablable.setText(QtGui.QApplication.translate("hotkey_edit", "can be disabled", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_keyChange.setText(QtGui.QApplication.translate("hotkey_edit", "can be changed", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_multiple.setText(QtGui.QApplication.translate("hotkey_edit", "allow multiple hotkeys", None, QtGui.QApplication.UnicodeUTF8))
        self.functionLabel.setText(QtGui.QApplication.translate("hotkey_edit", "function:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_functionMode.setItemText(0, QtGui.QApplication.translate("hotkey_edit", "run code", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_functionMode.setItemText(1, QtGui.QApplication.translate("hotkey_edit", "open file/url", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_functionMode.setItemText(2, QtGui.QApplication.translate("hotkey_edit", "send keystroke", None, QtGui.QApplication.UnicodeUTF8))
        self.functionButton.setText(QtGui.QApplication.translate("hotkey_edit", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeLabel.setText(QtGui.QApplication.translate("hotkey_edit", "scope:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeMode.setItemText(0, QtGui.QApplication.translate("hotkey_edit", "global", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeMode.setItemText(1, QtGui.QApplication.translate("hotkey_edit", "only in:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeMode.setItemText(2, QtGui.QApplication.translate("hotkey_edit", "not in:", None, QtGui.QApplication.UnicodeUTF8))
        self.scopePlus.setText(QtGui.QApplication.translate("hotkey_edit", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.scopeMinus.setText(QtGui.QApplication.translate("hotkey_edit", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeChange.setText(QtGui.QApplication.translate("hotkey_edit", "can be changed", None, QtGui.QApplication.UnicodeUTF8))

