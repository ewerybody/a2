# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\eric\io\code\a2\ui\a2widget\a2module_source_body.ui',
# licensing of 'C:\Users\eric\io\code\a2\ui\a2widget\a2module_source_body.ui' applies.
#
# Created: Tue Jul  3 17:33:51 2018
#      by: pyside2-uic  running on PySide2 5.11.1a1.dev1529944648
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(535, 156)
        self.modsource_layout = QtWidgets.QVBoxLayout(Form)
        self.modsource_layout.setObjectName("modsource_layout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setText("Maintainer:")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setText("Homepage:")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.homepage_label = QtWidgets.QLabel(self.frame)
        self.homepage_label.setText("x")
        self.homepage_label.setOpenExternalLinks(True)
        self.homepage_label.setObjectName("homepage_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.homepage_label)
        self.description_label = QtWidgets.QLabel(self.frame)
        self.description_label.setText("TextLabel")
        self.description_label.setObjectName("description_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.description_label)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setText("Version:")
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.maintainer_label = QtWidgets.QLabel(self.frame)
        self.maintainer_label.setText("x")
        self.maintainer_label.setObjectName("maintainer_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.maintainer_label)
        self.update_layout = QtWidgets.QHBoxLayout()
        self.update_layout.setObjectName("update_layout")
        self.version_label = QtWidgets.QLabel(self.frame)
        self.version_label.setText("x")
        self.version_label.setObjectName("version_label")
        self.update_layout.addWidget(self.version_label)
        self.update_button = QtWidgets.QPushButton(self.frame)
        self.update_button.setText("check for updates ...")
        self.update_button.setObjectName("update_button")
        self.update_layout.addWidget(self.update_button)
        self.a2option_button = A2MoreButton(self.frame)
        self.a2option_button.setText("")
        self.a2option_button.setAutoRaise(True)
        self.a2option_button.setObjectName("a2option_button")
        self.update_layout.addWidget(self.a2option_button)
        self.update_layout.setStretch(0, 1)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.update_layout)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setText("Local Folder:")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.local_path = A2PathField(self.frame)
        self.local_path.setObjectName("local_path")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.local_path)
        self.modsource_layout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from a2widget import A2PathField, A2MoreButton
