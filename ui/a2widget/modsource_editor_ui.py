# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\eric\io\code\a2\ui\a2widget\modsource_editor.ui',
# licensing of 'c:\Users\eric\io\code\a2\ui\a2widget\modsource_editor.ui' applies.
#
# Created: Thu Jun 25 11:45:14 2020
#      by: pyside2-uic  running on PySide2 5.15.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ModSourceUi(object):
    def setupUi(self, ModSourceUi):
        ModSourceUi.setObjectName("ModSourceUi")
        ModSourceUi.resize(747, 492)
        self.formLayout = QtWidgets.QFormLayout(ModSourceUi)
        self.formLayout.setObjectName("formLayout")
        self.news = A2CodeField(ModSourceUi)
        self.news.setObjectName("news")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.news)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.version_semantic = QtWidgets.QWidget(ModSourceUi)
        self.version_semantic.setObjectName("version_semantic")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.version_semantic)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.version_major = QtWidgets.QSpinBox(self.version_semantic)
        self.version_major.setObjectName("version_major")
        self.horizontalLayout_3.addWidget(self.version_major)
        self.version_minor = QtWidgets.QSpinBox(self.version_semantic)
        self.version_minor.setObjectName("version_minor")
        self.horizontalLayout_3.addWidget(self.version_minor)
        self.version_patch = QtWidgets.QSpinBox(self.version_semantic)
        self.version_patch.setObjectName("version_patch")
        self.horizontalLayout_3.addWidget(self.version_patch)
        self.horizontalLayout.addWidget(self.version_semantic)
        self.version_str = QtWidgets.QLineEdit(ModSourceUi)
        self.version_str.setObjectName("version_str")
        self.horizontalLayout.addWidget(self.version_str)
        self.version_str_check = QtWidgets.QCheckBox(ModSourceUi)
        self.version_str_check.setObjectName("version_str_check")
        self.horizontalLayout.addWidget(self.version_str_check)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(ModSourceUi)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(ModSourceUi)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.maintainer = QtWidgets.QLineEdit(ModSourceUi)
        self.maintainer.setObjectName("maintainer")
        self.horizontalLayout_2.addWidget(self.maintainer)
        self.label_4 = QtWidgets.QLabel(ModSourceUi)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.maintainer_at = QtWidgets.QLineEdit(ModSourceUi)
        self.maintainer_at.setObjectName("maintainer_at")
        self.horizontalLayout_2.addWidget(self.maintainer_at)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_5 = QtWidgets.QLabel(ModSourceUi)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.description = QtWidgets.QLineEdit(ModSourceUi)
        self.description.setObjectName("description")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.description)
        self.url = QtWidgets.QLineEdit(ModSourceUi)
        self.url.setObjectName("url")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.url)
        self.update_url = QtWidgets.QLineEdit(ModSourceUi)
        self.update_url.setObjectName("update_url")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.update_url)
        self.label_7 = QtWidgets.QLabel(ModSourceUi)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_6 = QtWidgets.QLabel(ModSourceUi)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ModSourceUi)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.busy_icon = BusyIcon(ModSourceUi)
        self.busy_icon.setText("")
        self.busy_icon.setObjectName("busy_icon")
        self.verticalLayout.addWidget(self.busy_icon)
        self.github_commits_btn = QtWidgets.QPushButton(ModSourceUi)
        self.github_commits_btn.setObjectName("github_commits_btn")
        self.verticalLayout.addWidget(self.github_commits_btn)
        self.verticalLayout.setStretch(2, 1)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(ModSourceUi)
        QtCore.QMetaObject.connectSlotsByName(ModSourceUi)

    def retranslateUi(self, ModSourceUi):
        ModSourceUi.setWindowTitle(QtWidgets.QApplication.translate("ModSourceUi", "Form", None, -1))
        self.version_str_check.setText(QtWidgets.QApplication.translate("ModSourceUi", "String", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("ModSourceUi", "version", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("ModSourceUi", "maintainer", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("ModSourceUi", "@", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("ModSourceUi", "description", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("ModSourceUi", "url", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("ModSourceUi", "update url", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("ModSourceUi", "news", None, -1))
        self.github_commits_btn.setText(QtWidgets.QApplication.translate("ModSourceUi", "Get from\n"
"GitHub\n"
"commits", None, -1))

from a2widget.a2text_field import A2CodeField
from a2widget.a2module_source import BusyIcon