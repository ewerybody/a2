# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'a2settings_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2hotkey import A2Hotkey


class Ui_a2settings(object):
    def setupUi(self, a2settings):
        if not a2settings.objectName():
            a2settings.setObjectName(u"a2settings")

        self.a2settings_view_layout = QVBoxLayout(a2settings)
        self.a2settings_view_layout.setObjectName(u"a2settings_view_layout")
        self.a2settings_view_layout.setContentsMargins(0, 0, 0, 0)
        self.a2settings_tab = QTabWidget(a2settings)
        self.a2settings_tab.setObjectName(u"a2settings_tab")
        self.main_tab = QWidget()
        self.main_tab.setObjectName(u"main_tab")
        self.verticalLayout = QVBoxLayout(self.main_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_3 = QLabel(self.main_tab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setText(u"Open a2 Dialog")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.a2hotkey = A2Hotkey(self.main_tab)
        self.a2hotkey.setObjectName(u"a2hotkey")
        self.a2hotkey.setEnabled(True)
        self.a2hotkey.setText(u"Win+Shift+A")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.a2hotkey)

        self.remember_selection = QCheckBox(self.main_tab)
        self.remember_selection.setObjectName(u"remember_selection")
        self.remember_selection.setText(u"Remember last selected Module")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.remember_selection)

        self.groupBox = QGroupBox(self.main_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setTitle(u"Integration")
        self.integrations_layout = QVBoxLayout(self.groupBox)
        self.integrations_layout.setObjectName(u"integrations_layout")
        self.integrations_layout.setContentsMargins(11, 25, 11, 11)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.groupBox)

        self.module_source_box = QGroupBox(self.main_tab)
        self.module_source_box.setObjectName(u"module_source_box")
        self.module_source_box.setTitle(u"Module Sources")
        self.mod_source_box_layout = QVBoxLayout(self.module_source_box)
        self.mod_source_box_layout.setSpacing(10)
        self.mod_source_box_layout.setObjectName(u"mod_source_box_layout")
        self.mod_source_box_layout.setContentsMargins(-1, 25, -1, -1)
        self.mod_source_layout = QVBoxLayout()
        self.mod_source_layout.setObjectName(u"mod_source_layout")

        self.mod_source_box_layout.addLayout(self.mod_source_layout)

        self.no_sources_msg = QLabel(self.module_source_box)
        self.no_sources_msg.setObjectName(u"no_sources_msg")
        self.no_sources_msg.setText(u"Currently there are no modules sources listed.\n"
"Go ahead and add or create one:")
        self.no_sources_msg.setAlignment(Qt.AlignCenter)
        self.no_sources_msg.setWordWrap(True)

        self.mod_source_box_layout.addWidget(self.no_sources_msg)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.a2add_button = QPushButton(self.module_source_box)
        self.a2add_button.setObjectName(u"a2add_button")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.a2add_button.sizePolicy().hasHeightForWidth())
        self.a2add_button.setSizePolicy(sizePolicy)
        self.a2add_button.setText(u"Add Source")

        self.horizontalLayout.addWidget(self.a2add_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.mod_source_box_layout.addLayout(self.horizontalLayout)


        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.module_source_box)


        self.verticalLayout.addLayout(self.formLayout)

        self.a2settings_tab.addTab(self.main_tab, "")
        self.a2settings_tab.setTabText(self.a2settings_tab.indexOf(self.main_tab), u"a2 Settings")
        self.advanced_tab = QWidget()
        self.advanced_tab.setObjectName(u"advanced_tab")
        self.a2settings_tab.addTab(self.advanced_tab, "")
        self.a2settings_tab.setTabText(self.a2settings_tab.indexOf(self.advanced_tab), u"Advanced")
        self.database_tab = QWidget()
        self.database_tab.setObjectName(u"database_tab")
        self.verticalLayout_5 = QVBoxLayout(self.database_tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.db_print_all_button = QPushButton(self.database_tab)
        self.db_print_all_button.setObjectName(u"db_print_all_button")
        self.db_print_all_button.setText(u"get db digest")

        self.verticalLayout_5.addWidget(self.db_print_all_button)

        self.db_printout = QTextEdit(self.database_tab)
        self.db_printout.setObjectName(u"db_printout")
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(10)
        self.db_printout.setFont(font)
        self.db_printout.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.db_printout)

        self.a2settings_tab.addTab(self.database_tab, "")
        self.a2settings_tab.setTabText(self.a2settings_tab.indexOf(self.database_tab), u"Database View")
        self.licenses_tab = QWidget()
        self.licenses_tab.setObjectName(u"licenses_tab")
        self.a2settings_tab.addTab(self.licenses_tab, "")
        self.a2settings_tab.setTabText(self.a2settings_tab.indexOf(self.licenses_tab), u"Licenses")
        self.console_tab = QWidget()
        self.console_tab.setObjectName(u"console_tab")
        self.a2settings_tab.addTab(self.console_tab, "")
        self.a2settings_tab.setTabText(self.a2settings_tab.indexOf(self.console_tab), u"Console")

        self.a2settings_view_layout.addWidget(self.a2settings_tab)


        self.retranslateUi(a2settings)

        self.a2settings_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(a2settings)
    # setupUi

    def retranslateUi(self, a2settings):
        pass
    # retranslateUi

