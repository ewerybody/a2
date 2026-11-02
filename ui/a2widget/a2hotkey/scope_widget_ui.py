"""
Form generated from reading UI file 'scope_widget.ui'

Created by: Qt User Interface Compiler version 6.12.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt

from a2widget.a2button_field import A2ButtonField
from a2widget.a2list import A2ListCompact


class Ui_ScopeWidget:
    def setupUi(self, ScopeWidget):
        if not ScopeWidget.objectName():
            ScopeWidget.setObjectName('ScopeWidget')
        ScopeWidget.setWindowTitle('Form')
        ScopeWidget.setToolTip('')
        self.verticalLayout = QVBoxLayout(ScopeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName('verticalLayout')
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.type_radio_widget = QWidget(ScopeWidget)
        self.type_radio_widget.setObjectName('type_radio_widget')
        self.horizontalLayout = QHBoxLayout(self.type_radio_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.scopeMode_0 = QRadioButton(self.type_radio_widget)
        self.scopeMode_0.setObjectName('scopeMode_0')
        self.scopeMode_0.setChecked(True)
        self.horizontalLayout.addWidget(self.scopeMode_0)
        self.scopeMode_1 = QRadioButton(self.type_radio_widget)
        self.scopeMode_1.setObjectName('scopeMode_1')
        self.scopeMode_1.setChecked(False)
        self.horizontalLayout.addWidget(self.scopeMode_1)
        self.scopeMode_2 = QRadioButton(self.type_radio_widget)
        self.scopeMode_2.setObjectName('scopeMode_2')
        self.scopeMode_2.setChecked(False)
        self.horizontalLayout.addWidget(self.scopeMode_2)
        self.horizontalLayout_2.addWidget(self.type_radio_widget, 0, Qt.AlignLeft)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer)
        self.scope_help = QToolButton(ScopeWidget)
        self.scope_help.setObjectName('scope_help')
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scope_help.sizePolicy().hasHeightForWidth())
        self.scope_help.setSizePolicy(sizePolicy)
        self.scope_help.setMaximumSize(QSize(50, 35))
        self.scope_help.setToolTip('Help on Scopes')
        self.scope_help.setText('h')
        self.scope_help.setAutoRaise(True)
        self.horizontalLayout_2.addWidget(self.scope_help)
        self.tool_buttons_widget = QWidget(ScopeWidget)
        self.tool_buttons_widget.setObjectName('tool_buttons_widget')
        self.horizontalLayout_3 = QHBoxLayout(self.tool_buttons_widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.scope_pick = QToolButton(self.tool_buttons_widget)
        self.scope_pick.setObjectName('scope_pick')
        sizePolicy.setHeightForWidth(self.scope_pick.sizePolicy().hasHeightForWidth())
        self.scope_pick.setSizePolicy(sizePolicy)
        self.scope_pick.setMaximumSize(QSize(50, 35))
        self.scope_pick.setToolTip('Pick from a Window')
        self.scope_pick.setText('p')
        self.scope_pick.setAutoRaise(True)
        self.horizontalLayout_3.addWidget(self.scope_pick)
        self.scope_delete = QToolButton(self.tool_buttons_widget)
        self.scope_delete.setObjectName('scope_delete')
        sizePolicy.setHeightForWidth(self.scope_delete.sizePolicy().hasHeightForWidth())
        self.scope_delete.setSizePolicy(sizePolicy)
        self.scope_delete.setMaximumSize(QSize(50, 35))
        self.scope_delete.setToolTip('Delete Selected Scope')
        self.scope_delete.setText('-')
        self.scope_delete.setAutoRaise(True)
        self.horizontalLayout_3.addWidget(self.scope_delete)
        self.scope_add = QToolButton(self.tool_buttons_widget)
        self.scope_add.setObjectName('scope_add')
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scope_add.sizePolicy().hasHeightForWidth())
        self.scope_add.setSizePolicy(sizePolicy1)
        self.scope_add.setMaximumSize(QSize(50, 35))
        self.scope_add.setToolTip('Add a Scope')
        self.scope_add.setText('+')
        self.scope_add.setAutoRaise(True)
        self.horizontalLayout_3.addWidget(self.scope_add)
        self.horizontalLayout_2.addWidget(self.tool_buttons_widget, 0, Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.cfg_scope = A2ListCompact(ScopeWidget)
        self.cfg_scope.setObjectName('cfg_scope')
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cfg_scope.sizePolicy().hasHeightForWidth())
        self.cfg_scope.setSizePolicy(sizePolicy2)
        self.cfg_scope.setMinimumSize(QSize(500, 40))
        self.cfg_scope.setMaximumSize(QSize(16777215, 16777215))
        self.cfg_scope.setToolTip('')
        self.cfg_scope.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalLayout.addWidget(self.cfg_scope)
        self.fields_widget = QWidget(ScopeWidget)
        self.fields_widget.setObjectName('fields_widget')
        self.formLayout_2 = QFormLayout(self.fields_widget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName('formLayout_2')
        self.label_2 = QLabel(self.fields_widget)
        self.label_2.setObjectName('label_2')
        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)
        self.scope_title = A2ButtonField(self.fields_widget)
        self.scope_title.setObjectName('scope_title')
        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.scope_title)
        self.label_3 = QLabel(self.fields_widget)
        self.label_3.setObjectName('label_3')
        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)
        self.scope_class = A2ButtonField(self.fields_widget)
        self.scope_class.setObjectName('scope_class')
        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.scope_class)
        self.label_4 = QLabel(self.fields_widget)
        self.label_4.setObjectName('label_4')
        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_4)
        self.scope_exe = A2ButtonField(self.fields_widget)
        self.scope_exe.setObjectName('scope_exe')
        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.scope_exe)
        self.verticalLayout.addWidget(self.fields_widget)
        QMetaObject.connectSlotsByName(ScopeWidget)
        self.scopeMode_0.setToolTip(
            QCoreApplication.translate('ScopeWidget', 'global - Makes it work anywhere in the system.', None)
        )
        self.scopeMode_0.setText(QCoreApplication.translate('ScopeWidget', 'golbal', None))
        self.scopeMode_1.setToolTip(
            QCoreApplication.translate('ScopeWidget', 'include - To make it work ONLY in certain windows.', None)
        )
        self.scopeMode_1.setText(QCoreApplication.translate('ScopeWidget', 'include:', None))
        self.scopeMode_2.setToolTip(
            QCoreApplication.translate(
                'ScopeWidget', 'exclude - To make it work anywhere BUT not in given windows.', None
            )
        )
        self.scopeMode_2.setText(QCoreApplication.translate('ScopeWidget', 'exclude:', None))
        self.label_2.setText(QCoreApplication.translate('ScopeWidget', 'title', None))
        self.label_3.setText(QCoreApplication.translate('ScopeWidget', 'window class', None))
        self.label_4.setText(QCoreApplication.translate('ScopeWidget', 'executable', None))
