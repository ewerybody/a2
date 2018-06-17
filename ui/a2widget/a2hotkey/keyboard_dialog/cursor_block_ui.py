# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\keyboard_dialog\cursor_block.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\keyboard_dialog\cursor_block.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CursorBlock(object):
    def setupUi(self, CursorBlock):
        CursorBlock.setObjectName("CursorBlock")
        CursorBlock.resize(368, 234)
        self.verticalLayout = QtWidgets.QVBoxLayout(CursorBlock)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.print_block = QtWidgets.QHBoxLayout()
        self.print_block.setObjectName("print_block")
        self.printscreen = QtWidgets.QPushButton(CursorBlock)
        self.printscreen.setText("Print\n"
"Screen")
        self.printscreen.setObjectName("printscreen")
        self.print_block.addWidget(self.printscreen)
        self.scrolllock = QtWidgets.QPushButton(CursorBlock)
        self.scrolllock.setText("Scroll\n"
"Lock")
        self.scrolllock.setObjectName("scrolllock")
        self.print_block.addWidget(self.scrolllock)
        self.pause = QtWidgets.QPushButton(CursorBlock)
        self.pause.setText("Pause")
        self.pause.setObjectName("pause")
        self.print_block.addWidget(self.pause)
        self.print_spacer = QtWidgets.QWidget(CursorBlock)
        self.print_spacer.setObjectName("print_spacer")
        self.print_block.addWidget(self.print_spacer)
        self.verticalLayout.addLayout(self.print_block)
        self.f_spacer = QtWidgets.QWidget(CursorBlock)
        self.f_spacer.setObjectName("f_spacer")
        self.verticalLayout.addWidget(self.f_spacer)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.delete = QtWidgets.QPushButton(CursorBlock)
        self.delete.setText("Del")
        self.delete.setObjectName("delete")
        self.gridLayout.addWidget(self.delete, 1, 0, 1, 1)
        self.end = QtWidgets.QPushButton(CursorBlock)
        self.end.setText("End")
        self.end.setObjectName("end")
        self.gridLayout.addWidget(self.end, 1, 1, 1, 1)
        self.down = QtWidgets.QPushButton(CursorBlock)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.down.setFont(font)
        self.down.setText("d")
        self.down.setObjectName("down")
        self.gridLayout.addWidget(self.down, 4, 1, 1, 1)
        self.insert = QtWidgets.QPushButton(CursorBlock)
        self.insert.setText("Insert")
        self.insert.setObjectName("insert")
        self.gridLayout.addWidget(self.insert, 0, 0, 1, 1)
        self.pgup = QtWidgets.QPushButton(CursorBlock)
        self.pgup.setText("Page\n"
"Up")
        self.pgup.setObjectName("pgup")
        self.gridLayout.addWidget(self.pgup, 0, 2, 1, 1)
        self.left = QtWidgets.QPushButton(CursorBlock)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.left.setFont(font)
        self.left.setText("l")
        self.left.setObjectName("left")
        self.gridLayout.addWidget(self.left, 4, 0, 1, 1)
        self.home = QtWidgets.QPushButton(CursorBlock)
        self.home.setText("Home")
        self.home.setObjectName("home")
        self.gridLayout.addWidget(self.home, 0, 1, 1, 1)
        self.up = QtWidgets.QPushButton(CursorBlock)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.up.setFont(font)
        self.up.setText("u")
        self.up.setObjectName("up")
        self.gridLayout.addWidget(self.up, 3, 1, 1, 1)
        self.pgdn = QtWidgets.QPushButton(CursorBlock)
        self.pgdn.setText("Page\n"
"Down")
        self.pgdn.setObjectName("pgdn")
        self.gridLayout.addWidget(self.pgdn, 1, 2, 1, 1)
        self.right = QtWidgets.QPushButton(CursorBlock)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.right.setFont(font)
        self.right.setText("r")
        self.right.setObjectName("right")
        self.gridLayout.addWidget(self.right, 4, 2, 1, 1)
        self.f_spacer_2 = QtWidgets.QWidget(CursorBlock)
        self.f_spacer_2.setObjectName("f_spacer_2")
        self.gridLayout.addWidget(self.f_spacer_2, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(CursorBlock)
        QtCore.QMetaObject.connectSlotsByName(CursorBlock)

    def retranslateUi(self, CursorBlock):
        CursorBlock.setWindowTitle(QtWidgets.QApplication.translate("CursorBlock", "Form", None, -1))

