# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2module_source.ui'
#
# Created: Mon May  7 17:24:02 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(560, 188)
        self.modsource_layout = QtGui.QVBoxLayout(Form)
        self.modsource_layout.setObjectName("modsource_layout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tool_button = QtGui.QToolButton(Form)
        self.tool_button.setText("...")
        self.tool_button.setAutoRaise(True)
        self.tool_button.setArrowType(QtCore.Qt.RightArrow)
        self.tool_button.setObjectName("tool_button")
        self.horizontalLayout.addWidget(self.tool_button)
        self.check = QtGui.QCheckBox(Form)
        self.check.setText("CheckBox")
        self.check.setObjectName("check")
        self.horizontalLayout.addWidget(self.check)
        self.mod_count = QtGui.QLabel(Form)
        self.mod_count.setText("TextLabel")
        self.mod_count.setObjectName("mod_count")
        self.horizontalLayout.addWidget(self.mod_count)
        self.error_icon = QtGui.QToolButton(Form)
        self.error_icon.setEnabled(False)
        self.error_icon.setText("...")
        self.error_icon.setAutoRaise(True)
        self.error_icon.setArrowType(QtCore.Qt.NoArrow)
        self.error_icon.setObjectName("error_icon")
        self.horizontalLayout.addWidget(self.error_icon)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.modsource_layout.addLayout(self.horizontalLayout)
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.formLayout = QtGui.QFormLayout(self.frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setText("Maintainer:")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setText("Homepage:")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.homepage_label = QtGui.QLabel(self.frame)
        self.homepage_label.setText("x")
        self.homepage_label.setOpenExternalLinks(True)
        self.homepage_label.setObjectName("homepage_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.homepage_label)
        self.description_label = QtGui.QLabel(self.frame)
        self.description_label.setText("TextLabel")
        self.description_label.setObjectName("description_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.description_label)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setText("Version:")
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.maintainer_label = QtGui.QLabel(self.frame)
        self.maintainer_label.setText("x")
        self.maintainer_label.setObjectName("maintainer_label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.maintainer_label)
        self.update_layout = QtGui.QHBoxLayout()
        self.update_layout.setObjectName("update_layout")
        self.version_label = QtGui.QLabel(self.frame)
        self.version_label.setText("x")
        self.version_label.setObjectName("version_label")
        self.update_layout.addWidget(self.version_label)
        self.update_button = QtGui.QPushButton(self.frame)
        self.update_button.setText("check for updates ...")
        self.update_button.setObjectName("update_button")
        self.update_layout.addWidget(self.update_button)
        self.version_tool_button = QtGui.QToolButton(self.frame)
        self.version_tool_button.setText("...")
        self.version_tool_button.setAutoRaise(True)
        self.version_tool_button.setArrowType(QtCore.Qt.DownArrow)
        self.version_tool_button.setObjectName("version_tool_button")
        self.update_layout.addWidget(self.version_tool_button)
        self.update_layout.setStretch(0, 1)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.update_layout)
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setText("Local Folder:")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.local_path = A2PathField(self.frame)
        self.local_path.setObjectName("local_path")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.local_path)
        self.modsource_layout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

from a2widget.a2path_field import A2PathField
