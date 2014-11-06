# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2design.ui'
#
# Created: Wed Nov  5 19:33:21 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_a2Widget(QtGui.QWidget):
    def setupUi(self, a2Widget):
        a2Widget.setObjectName("a2Widget")
        a2Widget.resize(1040, 513)
        a2Widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout_3 = QtGui.QVBoxLayout(a2Widget)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtGui.QSplitter(a2Widget)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtGui.QFrame.Plain)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.moduleBox = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moduleBox.sizePolicy().hasHeightForWidth())
        self.moduleBox.setSizePolicy(sizePolicy)
        self.moduleBox.setMinimumSize(QtCore.QSize(100, 0))
        self.moduleBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.moduleBox.setBaseSize(QtCore.QSize(26, 0))
        self.moduleBox.setObjectName("moduleBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.moduleBox)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.modList = QtGui.QListWidget(self.moduleBox)
        self.modList.setObjectName("modList")
        self.verticalLayout_2.addWidget(self.modList)
        self.settingsBox = QtGui.QGroupBox(self.splitter)
        self.settingsBox.setObjectName("settingsBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.settingsBox)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(self.settingsBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaContents = QtGui.QWidget()
        self.scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 606, 462))
        self.scrollAreaContents.setObjectName("scrollAreaContents")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.welcomeText = QtGui.QLabel(self.scrollAreaContents)
        self.welcomeText.setAutoFillBackground(False)
        self.welcomeText.setWordWrap(True)
        self.welcomeText.setObjectName("welcomeText")
        self.verticalLayout_4.addWidget(self.welcomeText)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout_3.addWidget(self.splitter)

        self.retranslateUi(a2Widget)
        QtCore.QMetaObject.connectSlotsByName(a2Widget)

    def retranslateUi(self, a2Widget):
        a2Widget.setWindowTitle(QtGui.QApplication.translate("a2Widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.moduleBox.setTitle(QtGui.QApplication.translate("a2Widget", "modules", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsBox.setTitle(QtGui.QApplication.translate("a2Widget", "settings", None, QtGui.QApplication.UnicodeUTF8))
        self.welcomeText.setText(QtGui.QApplication.translate("a2Widget", "Hello user! Welcome to a2! This is a template introduction Text. So far there is not much to say. I just wanted this to fill up more than one line properly. Voila!", None, QtGui.QApplication.UnicodeUTF8))

