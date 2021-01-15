# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modsource_editor.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2text_field import A2CodeField
from a2widget.a2module_source import BusyIcon


class Ui_ModSourceUi(object):
    def setupUi(self, ModSourceUi):
        if not ModSourceUi.objectName():
            ModSourceUi.setObjectName(u"ModSourceUi")

        self.formLayout = QFormLayout(ModSourceUi)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)
        self.news = A2CodeField(ModSourceUi)
        self.news.setObjectName(u"news")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.news)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.version_semantic = QWidget(ModSourceUi)
        self.version_semantic.setObjectName(u"version_semantic")
        self.horizontalLayout_3 = QHBoxLayout(self.version_semantic)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.version_major = QSpinBox(self.version_semantic)
        self.version_major.setObjectName(u"version_major")

        self.horizontalLayout_3.addWidget(self.version_major)

        self.version_minor = QSpinBox(self.version_semantic)
        self.version_minor.setObjectName(u"version_minor")

        self.horizontalLayout_3.addWidget(self.version_minor)

        self.version_patch = QSpinBox(self.version_semantic)
        self.version_patch.setObjectName(u"version_patch")

        self.horizontalLayout_3.addWidget(self.version_patch)


        self.horizontalLayout.addWidget(self.version_semantic)

        self.version_str = QLineEdit(ModSourceUi)
        self.version_str.setObjectName(u"version_str")

        self.horizontalLayout.addWidget(self.version_str)

        self.version_str_check = QCheckBox(ModSourceUi)
        self.version_str_check.setObjectName(u"version_str_check")

        self.horizontalLayout.addWidget(self.version_str_check)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(ModSourceUi)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(ModSourceUi)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.maintainer = QLineEdit(ModSourceUi)
        self.maintainer.setObjectName(u"maintainer")

        self.horizontalLayout_2.addWidget(self.maintainer)

        self.label_4 = QLabel(ModSourceUi)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.maintainer_at = QLineEdit(ModSourceUi)
        self.maintainer_at.setObjectName(u"maintainer_at")

        self.horizontalLayout_2.addWidget(self.maintainer_at)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_5 = QLabel(ModSourceUi)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.description = QLineEdit(ModSourceUi)
        self.description.setObjectName(u"description")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.description)

        self.url = QLineEdit(ModSourceUi)
        self.url.setObjectName(u"url")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.url)

        self.update_url = QLineEdit(ModSourceUi)
        self.update_url.setObjectName(u"update_url")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.update_url)

        self.label_7 = QLabel(ModSourceUi)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.label_6 = QLabel(ModSourceUi)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ModSourceUi)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTop|Qt.AlignTrailing)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignTop)

        self.busy_icon = BusyIcon(ModSourceUi)
        self.busy_icon.setObjectName(u"busy_icon")

        self.verticalLayout.addWidget(self.busy_icon)

        self.github_commits_btn = QPushButton(ModSourceUi)
        self.github_commits_btn.setObjectName(u"github_commits_btn")

        self.verticalLayout.addWidget(self.github_commits_btn)

        self.verticalLayout.setStretch(2, 1)

        self.formLayout.setLayout(3, QFormLayout.LabelRole, self.verticalLayout)


        self.retranslateUi(ModSourceUi)

        QMetaObject.connectSlotsByName(ModSourceUi)
    # setupUi

    def retranslateUi(self, ModSourceUi):
        ModSourceUi.setWindowTitle(QCoreApplication.translate("ModSourceUi", u"Form", None))
        self.version_str_check.setText(QCoreApplication.translate("ModSourceUi", u"String", None))
        self.label_2.setText(QCoreApplication.translate("ModSourceUi", u"version", None))
        self.label_3.setText(QCoreApplication.translate("ModSourceUi", u"maintainer", None))
        self.label_4.setText(QCoreApplication.translate("ModSourceUi", u"@", None))
        self.label_5.setText(QCoreApplication.translate("ModSourceUi", u"description", None))
        self.label_7.setText(QCoreApplication.translate("ModSourceUi", u"url", None))
        self.label_6.setText(QCoreApplication.translate("ModSourceUi", u"update url", None))
        self.label.setText(QCoreApplication.translate("ModSourceUi", u"news", None))
        self.busy_icon.setText("")
        self.github_commits_btn.setText(QCoreApplication.translate("ModSourceUi", u"Get from\n"
"GitHub\n"
"commits", None))
    # retranslateUi

