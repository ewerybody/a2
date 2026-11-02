"""
Form generated from reading UI file 'scope_dialog.ui'

Created by: Qt User Interface Compiler version 6.12.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import QHBoxLayout, QLabel, QLayout, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QCoreApplication, QMetaObject

from a2widget.a2hotkey.scope_widget import ScopeWidget


class Ui_ScopeDialog:
    def setupUi(self, ScopeDialog):
        if not ScopeDialog.objectName():
            ScopeDialog.setObjectName('ScopeDialog')
        ScopeDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(ScopeDialog)
        self.verticalLayout.setObjectName('verticalLayout')
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.display_only_label = QLabel(ScopeDialog)
        self.display_only_label.setObjectName('display_only_label')
        self.verticalLayout.addWidget(self.display_only_label)
        self.scope_widget = ScopeWidget(ScopeDialog)
        self.scope_widget.setObjectName('scope_widget')
        self.verticalLayout.addWidget(self.scope_widget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.a2ok_button = QPushButton(ScopeDialog)
        self.a2ok_button.setObjectName('a2ok_button')
        self.horizontalLayout.addWidget(self.a2ok_button)
        self.a2cancel_button = QPushButton(ScopeDialog)
        self.a2cancel_button.setObjectName('a2cancel_button')
        self.a2cancel_button.setFlat(True)
        self.horizontalLayout.addWidget(self.a2cancel_button)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        QWidget.setTabOrder(self.a2ok_button, self.a2cancel_button)
        self.retranslateUi(ScopeDialog)
        self.a2ok_button.clicked.connect(ScopeDialog.accept)
        self.a2cancel_button.clicked.connect(ScopeDialog.reject)
        QMetaObject.connectSlotsByName(ScopeDialog)

    def retranslateUi(self, ScopeDialog):
        ScopeDialog.setWindowTitle(QCoreApplication.translate('ScopeDialog', 'Dialog', None))
        self.display_only_label.setText(
            QCoreApplication.translate(
                'ScopeDialog',
                '<html><head/><body><p>This is for <span style=" font-weight:600;">display only</span>! The scope <span style=" font-weight:600;">cannot</span> be changed.</p></body></html>',
                None,
            )
        )
        self.a2ok_button.setText(QCoreApplication.translate('ScopeDialog', 'OK', None))
        self.a2cancel_button.setText(QCoreApplication.translate('ScopeDialog', 'Cancel', None))
