# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2scope_widget.ui'
#
# Created: Tue May  1 23:05:29 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ScopeWidget(object):
    def setupUi(self, ScopeWidget):
        ScopeWidget.setObjectName("ScopeWidget")
        ScopeWidget.resize(1202, 141)
        self.verticalLayout = QtGui.QVBoxLayout(ScopeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scopeRowLayout = QtGui.QHBoxLayout()
        self.scopeRowLayout.setContentsMargins(-1, 0, -1, -1)
        self.scopeRowLayout.setObjectName("scopeRowLayout")
        self.cfg_scopeMode = QtGui.QComboBox(ScopeWidget)
        self.cfg_scopeMode.setObjectName("cfg_scopeMode")
        self.cfg_scopeMode.addItem("")
        self.cfg_scopeMode.addItem("")
        self.cfg_scopeMode.addItem("")
        self.scopeRowLayout.addWidget(self.cfg_scopeMode)
        self.scope_add = QtGui.QPushButton(ScopeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scope_add.sizePolicy().hasHeightForWidth())
        self.scope_add.setSizePolicy(sizePolicy)
        self.scope_add.setMaximumSize(QtCore.QSize(50, 35))
        self.scope_add.setObjectName("scope_add")
        self.scopeRowLayout.addWidget(self.scope_add)
        self.scope_delete = QtGui.QPushButton(ScopeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scope_delete.sizePolicy().hasHeightForWidth())
        self.scope_delete.setSizePolicy(sizePolicy)
        self.scope_delete.setMaximumSize(QtCore.QSize(50, 35))
        self.scope_delete.setObjectName("scope_delete")
        self.scopeRowLayout.addWidget(self.scope_delete)
        self.cfg_scopeChange = QtGui.QCheckBox(ScopeWidget)
        self.cfg_scopeChange.setChecked(True)
        self.cfg_scopeChange.setObjectName("cfg_scopeChange")
        self.scopeRowLayout.addWidget(self.cfg_scopeChange)
        self.scopeRowLayout.setStretch(3, 1)
        self.verticalLayout.addLayout(self.scopeRowLayout)
        self.cfg_scope = QtGui.QListWidget(ScopeWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfg_scope.sizePolicy().hasHeightForWidth())
        self.cfg_scope.setSizePolicy(sizePolicy)
        self.cfg_scope.setMinimumSize(QtCore.QSize(0, 40))
        self.cfg_scope.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cfg_scope.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cfg_scope.setObjectName("cfg_scope")
        self.verticalLayout.addWidget(self.cfg_scope)

        self.retranslateUi(ScopeWidget)
        QtCore.QMetaObject.connectSlotsByName(ScopeWidget)

    def retranslateUi(self, ScopeWidget):
        ScopeWidget.setWindowTitle(QtGui.QApplication.translate("ScopeWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeMode.setItemText(0, QtGui.QApplication.translate("ScopeWidget", "global", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeMode.setItemText(1, QtGui.QApplication.translate("ScopeWidget", "only in:", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeMode.setItemText(2, QtGui.QApplication.translate("ScopeWidget", "not in:", None, QtGui.QApplication.UnicodeUTF8))
        self.scope_add.setText(QtGui.QApplication.translate("ScopeWidget", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.scope_delete.setText(QtGui.QApplication.translate("ScopeWidget", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.cfg_scopeChange.setText(QtGui.QApplication.translate("ScopeWidget", "can be changed", None, QtGui.QApplication.UnicodeUTF8))

