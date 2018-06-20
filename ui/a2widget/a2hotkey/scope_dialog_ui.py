# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\scope_dialog.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2hotkey\scope_dialog.ui' applies.
#
# Created: Sun Jun 17 23:09:57 2018
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_ScopeDialog(object):
    def setupUi(self, ScopeDialog):
        ScopeDialog.setObjectName("ScopeDialog")
        ScopeDialog.resize(472, 131)
        ScopeDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ScopeDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.display_only_label = QtWidgets.QLabel(ScopeDialog)
        self.display_only_label.setObjectName("display_only_label")
        self.verticalLayout.addWidget(self.display_only_label)
        self.scope_widget = ScopeWidget(ScopeDialog)
        self.scope_widget.setObjectName("scope_widget")
        self.verticalLayout.addWidget(self.scope_widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.a2ok_button = QtWidgets.QPushButton(ScopeDialog)
        self.a2ok_button.setObjectName("a2ok_button")
        self.horizontalLayout.addWidget(self.a2ok_button)
        self.a2cancel_button = QtWidgets.QPushButton(ScopeDialog)
        self.a2cancel_button.setFlat(True)
        self.a2cancel_button.setObjectName("a2cancel_button")
        self.horizontalLayout.addWidget(self.a2cancel_button)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ScopeDialog)
        QtCore.QObject.connect(self.a2ok_button, QtCore.SIGNAL("clicked()"), ScopeDialog.accept)
        QtCore.QObject.connect(self.a2cancel_button, QtCore.SIGNAL("clicked()"), ScopeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ScopeDialog)
        ScopeDialog.setTabOrder(self.a2ok_button, self.a2cancel_button)

    def retranslateUi(self, ScopeDialog):
        ScopeDialog.setWindowTitle(QtWidgets.QApplication.translate("ScopeDialog", "Dialog", None, -1))
        self.display_only_label.setText(QtWidgets.QApplication.translate("ScopeDialog", "<html><head/><body><p>This is for <span style=\" font-weight:600;\">display only</span>! The scope <span style=\" font-weight:600;\">cannot</span> be changed.</p></body></html>", None, -1))
        self.a2ok_button.setText(QtWidgets.QApplication.translate("ScopeDialog", "OK", None, -1))
        self.a2cancel_button.setText(QtWidgets.QApplication.translate("ScopeDialog", "Cancel", None, -1))

from a2widget.a2hotkey.scope_widget import ScopeWidget
