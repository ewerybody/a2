# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eRiC\io\code\a2\ui\a2ui.design.ui'
#
# Created: Fri Sep 12 22:28:51 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_a2(object):
    def setupUi(self, a2):
        a2.setObjectName("a2")
        a2.resize(1142, 856)
        a2.setWindowTitle("a2ui")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("a2logo 16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        a2.setWindowIcon(icon)
        a2.setAccessibleName("")
        self.centralwidget = QtGui.QWidget(a2)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_3.setMaximumSize(QtCore.QSize(0, 16777215))
        self.groupBox_3.setBaseSize(QtCore.QSize(300, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setContentsMargins(0, 5, 0, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtGui.QListWidget(self.groupBox_3)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtGui.QScrollArea(self.groupBox_4)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 754, 715))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtGui.QSpacerItem(20, 511, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.groupBox_4, 0, 1, 1, 2)
        a2.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(a2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1142, 38))
        self.menubar.setObjectName("menubar")
        self.menuA2 = QtGui.QMenu(self.menubar)
        self.menuA2.setObjectName("menuA2")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        a2.setMenuBar(self.menubar)
        self.actionExit = QtGui.QAction(a2)
        self.actionExit.setObjectName("actionExit")
        self.menuA2.addAction(self.actionExit)
        self.menubar.addAction(self.menuA2.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(a2)
        QtCore.QMetaObject.connectSlotsByName(a2)

    def retranslateUi(self, a2):
        self.groupBox_3.setTitle(QtGui.QApplication.translate("a2", "modules", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("a2", "module settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuA2.setTitle(QtGui.QApplication.translate("a2", "a2", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("a2", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("a2", "Exit", None, QtGui.QApplication.UnicodeUTF8))

