"""
Form generated from reading UI file 'button_edit.ui'

Created by: Qt User Interface Compiler version 6.12.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import QFormLayout, QLabel, QLineEdit
from PySide6.QtCore import QMetaObject, QSize, Qt

from a2widget.local_script import ScriptSelector


class Ui_edit:
    def setupUi(self, edit):
        if not edit.objectName():
            edit.setObjectName('edit')
        edit.setWindowTitle('Form')
        self.edit_layout = QFormLayout(edit)
        self.edit_layout.setObjectName('edit_layout')
        self.displayLabelLabel = QLabel(edit)
        self.displayLabelLabel.setObjectName('displayLabelLabel')
        self.displayLabelLabel.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel.setText('label text')
        self.displayLabelLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.displayLabelLabel)
        self.cfg_labeltext = QLineEdit(edit)
        self.cfg_labeltext.setObjectName('cfg_labeltext')
        self.cfg_labeltext.setText('')
        self.cfg_labeltext.setPlaceholderText('Space used by Button if empty!')
        self.edit_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfg_labeltext)
        self.displayLabelLabel_2 = QLabel(edit)
        self.displayLabelLabel_2.setObjectName('displayLabelLabel_2')
        self.displayLabelLabel_2.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_2.setText('button text')
        self.displayLabelLabel_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.displayLabelLabel_2)
        self.cfg_buttontext = QLineEdit(edit)
        self.cfg_buttontext.setObjectName('cfg_buttontext')
        self.cfg_buttontext.setPlaceholderText('Text to show on the Button.')
        self.edit_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfg_buttontext)
        self.displayLabelLabel_3 = QLabel(edit)
        self.displayLabelLabel_3.setObjectName('displayLabelLabel_3')
        self.displayLabelLabel_3.setMinimumSize(QSize(100, 0))
        self.displayLabelLabel_3.setText('python script')
        self.displayLabelLabel_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.edit_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.displayLabelLabel_3)
        self.script_selector = ScriptSelector(edit)
        self.script_selector.setObjectName('script_selector')
        self.edit_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.script_selector)
        QMetaObject.connectSlotsByName(edit)
