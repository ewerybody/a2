# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\ctrl.ui'
#
# Created: Thu May 28 01:10:17 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_EditCtrl(object):
    def setupUi(self, EditCtrl):
        EditCtrl.setObjectName("EditCtrl")
        EditCtrl.resize(1303, 176)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditCtrl.sizePolicy().hasHeightForWidth())
        EditCtrl.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(EditCtrl)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout = QtGui.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.horizontalLayout.addLayout(self.layout)
        self.ctrlButtonLayout = QtGui.QVBoxLayout()
        self.ctrlButtonLayout.setSpacing(0)
        self.ctrlButtonLayout.setObjectName("ctrlButtonLayout")
        self.ctrlButton = QtGui.QPushButton(EditCtrl)
        self.ctrlButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.ctrlButton.setObjectName("ctrlButton")
        self.ctrlButtonLayout.addWidget(self.ctrlButton)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.ctrlButtonLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.ctrlButtonLayout)
        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(EditCtrl)
        QtCore.QMetaObject.connectSlotsByName(EditCtrl)

    def retranslateUi(self, EditCtrl):
        self.ctrlButton.setText(QtGui.QApplication.translate("EditCtrl", "...", None, QtGui.QApplication.UnicodeUTF8))

