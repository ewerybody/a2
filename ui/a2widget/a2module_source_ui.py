# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2widget\a2module_source.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2widget\a2module_source.ui' applies.
#
# Created: Tue Jun 23 18:21:20 2020
#      by: pyside2-uic  running on PySide2 5.15.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(778, 67)
        self.modsource_layout = QtWidgets.QVBoxLayout(Form)
        self.modsource_layout.setContentsMargins(0, 0, 0, 0)
        self.modsource_layout.setObjectName("modsource_layout")
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setObjectName("header_layout")
        self.check = QtWidgets.QCheckBox(Form)
        self.check.setText("")
        self.check.setObjectName("check")
        self.header_layout.addWidget(self.check)
        self.tool_button = QtWidgets.QToolButton(Form)
        self.tool_button.setText("...")
        self.tool_button.setAutoRaise(True)
        self.tool_button.setArrowType(QtCore.Qt.RightArrow)
        self.tool_button.setObjectName("tool_button")
        self.header_layout.addWidget(self.tool_button)
        self.label_widget = QtWidgets.QWidget(Form)
        self.label_widget.setObjectName("label_widget")
        self.labels_layout = QtWidgets.QHBoxLayout(self.label_widget)
        self.labels_layout.setContentsMargins(0, 0, 0, 0)
        self.labels_layout.setObjectName("labels_layout")
        self.icon_label = QtWidgets.QLabel(self.label_widget)
        self.icon_label.setMinimumSize(QtCore.QSize(20, 20))
        self.icon_label.setText("")
        self.icon_label.setObjectName("icon_label")
        self.labels_layout.addWidget(self.icon_label)
        self.mod_label = QtWidgets.QLabel(self.label_widget)
        self.mod_label.setMinimumSize(QtCore.QSize(40, 0))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.mod_label.setFont(font)
        self.mod_label.setText("ModSourceName")
        self.mod_label.setObjectName("mod_label")
        self.labels_layout.addWidget(self.mod_label)
        self.extra_label = QtWidgets.QLabel(self.label_widget)
        self.extra_label.setMinimumSize(QtCore.QSize(40, 0))
        self.extra_label.setText("(extra)")
        self.extra_label.setObjectName("extra_label")
        self.labels_layout.addWidget(self.extra_label)
        self.mod_count = QtWidgets.QLabel(self.label_widget)
        self.mod_count.setText("TextLabel")
        self.mod_count.setAlignment(QtCore.Qt.AlignCenter)
        self.mod_count.setObjectName("mod_count")
        self.labels_layout.addWidget(self.mod_count)
        self.labels_layout.setStretch(3, 1)
        self.header_layout.addWidget(self.label_widget)
        self.error_icon = QtWidgets.QToolButton(Form)
        self.error_icon.setEnabled(False)
        self.error_icon.setText("...")
        self.error_icon.setAutoRaise(True)
        self.error_icon.setArrowType(QtCore.Qt.NoArrow)
        self.error_icon.setObjectName("error_icon")
        self.header_layout.addWidget(self.error_icon)
        self.header_layout.setStretch(2, 1)
        self.modsource_layout.addLayout(self.header_layout)
        self.details_widget = QtWidgets.QWidget(Form)
        self.details_widget.setObjectName("details_widget")
        self.modsource_layout.addWidget(self.details_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

