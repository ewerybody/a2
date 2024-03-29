# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'base.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QLayout, QLineEdit, QPushButton, 
    QVBoxLayout, QWidget)
from a2qt.QtGui import QFont
from a2qt.QtCore import QMetaObject, Qt

from a2widget.a2more_button import A2MoreButton

class Ui_Keyboard:
    def setupUi(self, Keyboard):
        if not Keyboard.objectName():
            Keyboard.setObjectName('Keyboard')
        Keyboard.setWindowTitle('Hotkey Dialog')
        self.dialog_layout = QVBoxLayout(Keyboard)
        self.dialog_layout.setObjectName('dialog_layout')
        self.dialog_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName('top_layout')
        self.top_layout.setContentsMargins(-1, 10, -1, 10)
        self.key_field = QLineEdit(Keyboard)
        self.key_field.setObjectName('key_field')
        self.key_field.setText('')
        self.key_field.setReadOnly(True)
        self.top_layout.addWidget(self.key_field)
        self.option_button = A2MoreButton(Keyboard)
        self.option_button.setObjectName('option_button')
        self.option_button.setText('...')
        self.top_layout.addWidget(self.option_button)
        self.label_2 = QLabel(Keyboard)
        self.label_2.setObjectName('label_2')
        self.label_2.setText('Show:')
        self.top_layout.addWidget(self.label_2)
        self.check_numpad = QCheckBox(Keyboard)
        self.check_numpad.setObjectName('check_numpad')
        self.check_numpad.setText('Num Pad')
        self.top_layout.addWidget(self.check_numpad)
        self.check_mouse = QCheckBox(Keyboard)
        self.check_mouse.setObjectName('check_mouse')
        self.check_mouse.setText('Mouse')
        self.top_layout.addWidget(self.check_mouse)
        self.dialog_layout.addLayout(self.top_layout)
        self.keys_widget = QWidget(Keyboard)
        self.keys_widget.setObjectName('keys_widget')
        self.keys_layout = QHBoxLayout(self.keys_widget)
        self.keys_layout.setObjectName('keys_layout')
        self.keys_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget = QWidget(self.keys_widget)
        self.main_widget.setObjectName('main_widget')
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setObjectName('main_layout')
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.f_row = QHBoxLayout()
        self.f_row.setObjectName('f_row')
        self.escape = QPushButton(self.main_widget)
        self.escape.setObjectName('escape')
        self.escape.setText('Esc')
        self.f_row.addWidget(self.escape)
        self.main_layout.addLayout(self.f_row)
        self.f_spacer = QWidget(self.main_widget)
        self.f_spacer.setObjectName('f_spacer')
        self.main_layout.addWidget(self.f_spacer)
        self.enter_key_rows = QHBoxLayout()
        self.enter_key_rows.setObjectName('enter_key_rows')
        self.top_letter_rows = QVBoxLayout()
        self.top_letter_rows.setObjectName('top_letter_rows')
        self.number_row = QHBoxLayout()
        self.number_row.setObjectName('number_row')
        self.backspace = QPushButton(self.main_widget)
        self.backspace.setObjectName('backspace')
        self.backspace.setText('Backspace')
        self.number_row.addWidget(self.backspace)
        self.top_letter_rows.addLayout(self.number_row)
        self.letter_row_top = QHBoxLayout()
        self.letter_row_top.setObjectName('letter_row_top')
        self.tab = QPushButton(self.main_widget)
        self.tab.setObjectName('tab')
        self.tab.setText('Tab')
        self.letter_row_top.addWidget(self.tab)
        self.top_letter_rows.addLayout(self.letter_row_top)
        self.enter_key_rows.addLayout(self.top_letter_rows)
        self.main_layout.addLayout(self.enter_key_rows)
        self.letter_row_middle = QHBoxLayout()
        self.letter_row_middle.setObjectName('letter_row_middle')
        self.capslock = QPushButton(self.main_widget)
        self.capslock.setObjectName('capslock')
        self.capslock.setText('Caps Lock')
        self.letter_row_middle.addWidget(self.capslock)
        self.main_layout.addLayout(self.letter_row_middle)
        self.letter_row_bottom = QHBoxLayout()
        self.letter_row_bottom.setObjectName('letter_row_bottom')
        self.lshift = QPushButton(self.main_widget)
        self.lshift.setObjectName('lshift')
        font = QFont()
        font.setBold(True)
        self.lshift.setFont(font)
        self.lshift.setText('Shift')
        self.letter_row_bottom.addWidget(self.lshift)
        self.rshift = QPushButton(self.main_widget)
        self.rshift.setObjectName('rshift')
        self.rshift.setFont(font)
        self.rshift.setText('Shift')
        self.letter_row_bottom.addWidget(self.rshift)
        self.main_layout.addLayout(self.letter_row_bottom)
        self.bottom_row = QHBoxLayout()
        self.bottom_row.setObjectName('bottom_row')
        self.lctrl = QPushButton(self.main_widget)
        self.lctrl.setObjectName('lctrl')
        self.lctrl.setFont(font)
        self.lctrl.setText('Ctrl')
        self.bottom_row.addWidget(self.lctrl)
        self.lwin = QPushButton(self.main_widget)
        self.lwin.setObjectName('lwin')
        self.lwin.setFont(font)
        self.lwin.setText('Win')
        self.bottom_row.addWidget(self.lwin)
        self.lalt = QPushButton(self.main_widget)
        self.lalt.setObjectName('lalt')
        self.lalt.setFont(font)
        self.lalt.setText('Alt')
        self.bottom_row.addWidget(self.lalt)
        self.space = QPushButton(self.main_widget)
        self.space.setObjectName('space')
        self.space.setText('Space')
        self.space.setCheckable(True)
        self.bottom_row.addWidget(self.space)
        self.ralt = QPushButton(self.main_widget)
        self.ralt.setObjectName('ralt')
        self.ralt.setFont(font)
        self.ralt.setText('Alt')
        self.bottom_row.addWidget(self.ralt)
        self.rwin = QPushButton(self.main_widget)
        self.rwin.setObjectName('rwin')
        self.rwin.setFont(font)
        self.rwin.setText('Win')
        self.bottom_row.addWidget(self.rwin)
        self.appskey = QPushButton(self.main_widget)
        self.appskey.setObjectName('appskey')
        self.appskey.setText('AppsKey')
        self.bottom_row.addWidget(self.appskey)
        self.rctrl = QPushButton(self.main_widget)
        self.rctrl.setObjectName('rctrl')
        self.rctrl.setFont(font)
        self.rctrl.setText('Ctrl')
        self.bottom_row.addWidget(self.rctrl)
        self.bottom_row.setStretch(3, 1)
        self.main_layout.addLayout(self.bottom_row)
        self.keys_layout.addWidget(self.main_widget)
        self.dialog_layout.addWidget(self.keys_widget)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setObjectName('bottom_layout')
        self.bottom_layout.setContentsMargins(-1, 15, -1, -1)
        self.a2ok_button = QPushButton(Keyboard)
        self.a2ok_button.setObjectName('a2ok_button')
        self.a2ok_button.setText('OK')
        self.bottom_layout.addWidget(self.a2ok_button)
        self.a2cancel_button = QPushButton(Keyboard)
        self.a2cancel_button.setObjectName('a2cancel_button')
        self.a2cancel_button.setText('Cancel')
        self.a2cancel_button.setFlat(True)
        self.bottom_layout.addWidget(self.a2cancel_button)
        self.bottom_layout.setStretch(0, 1)
        self.dialog_layout.addLayout(self.bottom_layout)
        self.i_know_checkbox = QCheckBox(Keyboard)
        self.i_know_checkbox.setObjectName('i_know_checkbox')
        self.i_know_checkbox.setText("I know what I'm doing!")
        self.dialog_layout.addWidget(self.i_know_checkbox, 0, Qt.AlignVCenter)
        self.dialog_layout.setStretch(1, 1)
        QMetaObject.connectSlotsByName(Keyboard)
