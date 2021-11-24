# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2module_list.ui'

Created by: Qt User Interface Compiler version 6.2.0

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from a2qt.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from a2qt.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLineEdit, QPushButton, QSizePolicy, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from a2widget.a2modlist import A2ModList
from a2widget.a2more_button import A2MoreButton

class Ui_ModuleList:
    def setupUi(self, ModuleList):
        if not ModuleList.objectName():
            ModuleList.setObjectName(u"ModuleList")
        ModuleList.setWindowTitle(u"Form")
        self.module_list_layout = QVBoxLayout(ModuleList)
        self.module_list_layout.setSpacing(5)
        self.module_list_layout.setObjectName(u"module_list_layout")
        self.module_list_layout.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_field = QLineEdit(ModuleList)
        self.search_field.setObjectName(u"search_field")
        self.horizontalLayout.addWidget(self.search_field)
        self.a2search_x_button = QPushButton(ModuleList)
        self.a2search_x_button.setObjectName(u"a2search_x_button")
        self.a2search_x_button.setFlat(True)
        self.horizontalLayout.addWidget(self.a2search_x_button)
        self.filter_menu_button = A2MoreButton(ModuleList)
        self.filter_menu_button.setObjectName(u"filter_menu_button")
        self.horizontalLayout.addWidget(self.filter_menu_button)
        self.module_list_layout.addLayout(self.horizontalLayout)
        self.a2module_list_widget = A2ModList(ModuleList)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.a2module_list_widget.setHeaderItem(__qtreewidgetitem)
        self.a2module_list_widget.setObjectName(u"a2module_list_widget")
        self.a2module_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.a2module_list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.a2module_list_widget.setProperty("showDropIndicator", False)
        self.a2module_list_widget.setAlternatingRowColors(True)
        self.a2module_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.a2module_list_widget.setIndentation(0)
        self.a2module_list_widget.setAnimated(True)
        self.a2module_list_widget.setColumnCount(1)
        self.a2module_list_widget.header().setVisible(False)
        self.module_list_layout.addWidget(self.a2module_list_widget)
        QMetaObject.connectSlotsByName(ModuleList)
