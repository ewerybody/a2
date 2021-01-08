# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cursor_block.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *


class Ui_CursorBlock(object):
    def setupUi(self, CursorBlock):
        if not CursorBlock.objectName():
            CursorBlock.setObjectName(u"CursorBlock")
        CursorBlock.resize(368, 234)
        self.verticalLayout = QVBoxLayout(CursorBlock)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.print_block = QHBoxLayout()
        self.print_block.setObjectName(u"print_block")
        self.printscreen = QPushButton(CursorBlock)
        self.printscreen.setObjectName(u"printscreen")
        self.printscreen.setText(u"Print\n"
"Screen")

        self.print_block.addWidget(self.printscreen)

        self.scrolllock = QPushButton(CursorBlock)
        self.scrolllock.setObjectName(u"scrolllock")
        self.scrolllock.setText(u"Scroll\n"
"Lock")

        self.print_block.addWidget(self.scrolllock)

        self.pause = QPushButton(CursorBlock)
        self.pause.setObjectName(u"pause")
        self.pause.setText(u"Pause")

        self.print_block.addWidget(self.pause)

        self.print_spacer = QWidget(CursorBlock)
        self.print_spacer.setObjectName(u"print_spacer")

        self.print_block.addWidget(self.print_spacer)


        self.verticalLayout.addLayout(self.print_block)

        self.f_spacer = QWidget(CursorBlock)
        self.f_spacer.setObjectName(u"f_spacer")

        self.verticalLayout.addWidget(self.f_spacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.delete = QPushButton(CursorBlock)
        self.delete.setObjectName(u"delete")
        self.delete.setText(u"Del")

        self.gridLayout.addWidget(self.delete, 1, 0, 1, 1)

        self.end = QPushButton(CursorBlock)
        self.end.setObjectName(u"end")
        self.end.setText(u"End")

        self.gridLayout.addWidget(self.end, 1, 1, 1, 1)

        self.down = QPushButton(CursorBlock)
        self.down.setObjectName(u"down")
        font = QFont()
        font.setBold(True)
        self.down.setFont(font)
        self.down.setText(u"d")

        self.gridLayout.addWidget(self.down, 4, 1, 1, 1)

        self.insert = QPushButton(CursorBlock)
        self.insert.setObjectName(u"insert")
        self.insert.setText(u"Insert")

        self.gridLayout.addWidget(self.insert, 0, 0, 1, 1)

        self.pgup = QPushButton(CursorBlock)
        self.pgup.setObjectName(u"pgup")
        self.pgup.setText(u"Page\n"
"Up")

        self.gridLayout.addWidget(self.pgup, 0, 2, 1, 1)

        self.left = QPushButton(CursorBlock)
        self.left.setObjectName(u"left")
        self.left.setFont(font)
        self.left.setText(u"l")

        self.gridLayout.addWidget(self.left, 4, 0, 1, 1)

        self.home = QPushButton(CursorBlock)
        self.home.setObjectName(u"home")
        self.home.setText(u"Home")

        self.gridLayout.addWidget(self.home, 0, 1, 1, 1)

        self.up = QPushButton(CursorBlock)
        self.up.setObjectName(u"up")
        self.up.setFont(font)
        self.up.setText(u"u")

        self.gridLayout.addWidget(self.up, 3, 1, 1, 1)

        self.pgdn = QPushButton(CursorBlock)
        self.pgdn.setObjectName(u"pgdn")
        self.pgdn.setText(u"Page\n"
"Down")

        self.gridLayout.addWidget(self.pgdn, 1, 2, 1, 1)

        self.right = QPushButton(CursorBlock)
        self.right.setObjectName(u"right")
        self.right.setFont(font)
        self.right.setText(u"r")

        self.gridLayout.addWidget(self.right, 4, 2, 1, 1)

        self.f_spacer_2 = QWidget(CursorBlock)
        self.f_spacer_2.setObjectName(u"f_spacer_2")

        self.gridLayout.addWidget(self.f_spacer_2, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(CursorBlock)

        QMetaObject.connectSlotsByName(CursorBlock)
    # setupUi

    def retranslateUi(self, CursorBlock):
        pass
    # retranslateUi

