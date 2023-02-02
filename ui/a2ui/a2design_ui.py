# -*- coding: utf-8 -*-

"""
Form generated from reading UI file 'a2design.ui'

Created by: Qt User Interface Compiler version 6.4.2

WARNING! All changes made in this file will be lost when recompiling UI file!
"""

from a2qt.QtGui import QAction, QFont
from a2qt.QtWidgets import QMenu, QMenuBar, QSplitter, QVBoxLayout, QWidget
from a2qt.QtCore import QMetaObject, QRect, QSize, Qt

from a2widget.a2module_list import A2ModuleList
from a2widget.a2module_view import A2ModuleView

class Ui_a2MainWindow:
    def setupUi(self, a2MainWindow):
        if not a2MainWindow.objectName():
            a2MainWindow.setObjectName('a2MainWindow')
        font = QFont()
        font.setPointSize(10)
        a2MainWindow.setFont(font)
        a2MainWindow.setWindowTitle('a2')
        self.actionAbout_a2 = QAction(a2MainWindow)
        self.actionAbout_a2.setObjectName('actionAbout_a2')
        self.actionAbout_a2.setText('About a2')
        self.actionEdit_module = QAction(a2MainWindow)
        self.actionEdit_module.setObjectName('actionEdit_module')
        self.actionEdit_module.setText('Edit Module')
        self.actionEdit_module.setShortcut('Ctrl+E')
        self.actionDisable_all_modules = QAction(a2MainWindow)
        self.actionDisable_all_modules.setObjectName('actionDisable_all_modules')
        self.actionDisable_all_modules.setText('Disable All Modules')
        self.actionExplore_to = QAction(a2MainWindow)
        self.actionExplore_to.setObjectName('actionExplore_to')
        self.actionExplore_to.setText('Explore to Module ...')
        self.actionExplore_to.setShortcut('Alt+E')
        self.actionAbout_Autohotkey = QAction(a2MainWindow)
        self.actionAbout_Autohotkey.setObjectName('actionAbout_Autohotkey')
        self.actionAbout_Autohotkey.setText('Autohotkey.com')
        self.actionExplore_to_a2_dir = QAction(a2MainWindow)
        self.actionExplore_to_a2_dir.setObjectName('actionExplore_to_a2_dir')
        self.actionExplore_to_a2_dir.setText('Explore to a2 ...')
        self.actionA2_settings = QAction(a2MainWindow)
        self.actionA2_settings.setObjectName('actionA2_settings')
        self.actionA2_settings.setText('a2 Settings')
        self.actionExit_a2ui = QAction(a2MainWindow)
        self.actionExit_a2ui.setObjectName('actionExit_a2ui')
        self.actionExit_a2ui.setText('Exit a2UI')
        self.actionRefresh_UI = QAction(a2MainWindow)
        self.actionRefresh_UI.setObjectName('actionRefresh_UI')
        self.actionRefresh_UI.setText('Refresh UI')
        self.actionRefresh_UI.setShortcut('F5')
        self.action_report_bug = QAction(a2MainWindow)
        self.action_report_bug.setObjectName('action_report_bug')
        self.action_report_bug.setText('Report a bug')
        self.actionNew_Module_Dialog = QAction(a2MainWindow)
        self.actionNew_Module_Dialog.setObjectName('actionNew_Module_Dialog')
        self.actionNew_Module_Dialog.setText('Create New Module')
        self.actionNew_Module_Dialog.setShortcut('Ctrl+N')
        self.actionBuild_A2_Package = QAction(a2MainWindow)
        self.actionBuild_A2_Package.setObjectName('actionBuild_A2_Package')
        self.actionBuild_A2_Package.setText('Build A2 Package')
        self.actionCreate_New_Element = QAction(a2MainWindow)
        self.actionCreate_New_Element.setObjectName('actionCreate_New_Element')
        self.actionCreate_New_Element.setText('Create New Element')
        self.actionCreate_New_Element.setShortcut('Ctrl+S')
        self.actionHelp_on_Module = QAction(a2MainWindow)
        self.actionHelp_on_Module.setObjectName('actionHelp_on_Module')
        self.actionHelp_on_Module.setText('Help on Module')
        self.actionRevert_Settings = QAction(a2MainWindow)
        self.actionRevert_Settings.setObjectName('actionRevert_Settings')
        self.actionRevert_Settings.setText('Revert Settings')
        self.actionRevert_Settings.setShortcut('Ctrl+S')
        self.actionReload_a2_Runtime = QAction(a2MainWindow)
        self.actionReload_a2_Runtime.setObjectName('actionReload_a2_Runtime')
        self.actionReload_a2_Runtime.setText('Reload a2 Runtime')
        self.actionReload_a2_Runtime.setShortcut('Ctrl+S')
        self.actionUnload_a2_Runtime = QAction(a2MainWindow)
        self.actionUnload_a2_Runtime.setObjectName('actionUnload_a2_Runtime')
        self.actionUnload_a2_Runtime.setText('Unload a2 Runtime')
        self.actionLoad_a2_Runtime = QAction(a2MainWindow)
        self.actionLoad_a2_Runtime.setObjectName('actionLoad_a2_Runtime')
        self.actionLoad_a2_Runtime.setText('Load a2 Runtime')
        self.actionExplore_to_a2_data_dir = QAction(a2MainWindow)
        self.actionExplore_to_a2_data_dir.setObjectName('actionExplore_to_a2_data_dir')
        self.actionExplore_to_a2_data_dir.setText('Explore to a2 data ...')
        self.actionUninstall_a2 = QAction(a2MainWindow)
        self.actionUninstall_a2.setObjectName('actionUninstall_a2')
        self.actionUninstall_a2.setText('Uninstall a2')
        self.action_report_sugg = QAction(a2MainWindow)
        self.action_report_sugg.setObjectName('action_report_sugg')
        self.action_report_sugg.setText('Suggest a feature')
        self.actionExport_Settings = QAction(a2MainWindow)
        self.actionExport_Settings.setObjectName('actionExport_Settings')
        self.actionExport_Settings.setText('Export Settings')
        self.actionImport_Settings = QAction(a2MainWindow)
        self.actionImport_Settings.setObjectName('actionImport_Settings')
        self.actionImport_Settings.setText('Import Settings')
        self.actionChat_on_Gitter = QAction(a2MainWindow)
        self.actionChat_on_Gitter.setObjectName('actionChat_on_Gitter')
        self.actionChat_on_Gitter.setText('Chat on Gitter')
        self.actionChat_on_Telegram = QAction(a2MainWindow)
        self.actionChat_on_Telegram.setObjectName('actionChat_on_Telegram')
        self.actionChat_on_Telegram.setText('Chat on Telegram')
        self.actionSet_a2_Version = QAction(a2MainWindow)
        self.actionSet_a2_Version.setObjectName('actionSet_a2_Version')
        self.actionSet_a2_Version.setText('Set a2 Version')
        self.actionInspect_UI = QAction(a2MainWindow)
        self.actionInspect_UI.setObjectName('actionInspect_UI')
        self.actionInspect_UI.setText('Inspect UI')
        self.actionInspect_UI.setShortcut('Ctrl+Shift+C')
        self.actiona2_on_github = QAction(a2MainWindow)
        self.actiona2_on_github.setObjectName('actiona2_on_github')
        self.actiona2_on_github.setText('a2 on github.com')
        self.action_updates = QAction(a2MainWindow)
        self.action_updates.setObjectName('action_updates')
        self.action_updates.setText('up-to-dateness')
        self.action_update_a2 = QAction(a2MainWindow)
        self.action_update_a2.setObjectName('action_update_a2')
        self.action_update_a2.setText('update_a2')
        self.action_update_packages = QAction(a2MainWindow)
        self.action_update_packages.setObjectName('action_update_packages')
        self.action_update_packages.setText('update_packages')
        self.centralwidget = QWidget(a2MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName('verticalLayout')
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName('splitter')
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.module_list = A2ModuleList(self.splitter)
        self.module_list.setObjectName('module_list')
        self.module_list.setMinimumSize(QSize(150, 0))
        self.module_list.setMaximumSize(QSize(500, 16777215))
        self.splitter.addWidget(self.module_list)
        self.module_view = A2ModuleView(self.splitter)
        self.module_view.setObjectName('module_view')
        self.module_view.setMinimumSize(QSize(500, 0))
        self.splitter.addWidget(self.module_view)
        self.verticalLayout.addWidget(self.splitter)
        a2MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(a2MainWindow)
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QRect(0, 0, 753, 29))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName('menuHelp')
        self.menuHelp.setTitle('&Help')
        self.menuDev = QMenu(self.menubar)
        self.menuDev.setObjectName('menuDev')
        self.menuDev.setTitle('&Dev')
        self.menuRollback_Changes = QMenu(self.menuDev)
        self.menuRollback_Changes.setObjectName('menuRollback_Changes')
        self.menuRollback_Changes.setTitle('Rollback Changes')
        self.menuMain = QMenu(self.menubar)
        self.menuMain.setObjectName('menuMain')
        self.menuMain.setTitle('&Main')
        self.menuModule = QMenu(self.menubar)
        self.menuModule.setObjectName('menuModule')
        self.menuModule.setTitle('Module')
        self.menuUpdates = QMenu(self.menubar)
        self.menuUpdates.setObjectName('menuUpdates')
        self.menuUpdates.setTitle('Update Available!')
        a2MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuModule.menuAction())
        self.menubar.addAction(self.menuDev.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuUpdates.menuAction())
        self.menuHelp.addAction(self.action_report_bug)
        self.menuHelp.addAction(self.action_report_sugg)
        self.menuHelp.addAction(self.actionChat_on_Gitter)
        self.menuHelp.addAction(self.actionChat_on_Telegram)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_Autohotkey)
        self.menuHelp.addAction(self.actiona2_on_github)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.action_updates)
        self.menuHelp.addAction(self.actionAbout_a2)
        self.menuDev.addAction(self.actionNew_Module_Dialog)
        self.menuDev.addAction(self.actionEdit_module)
        self.menuDev.addAction(self.actionExplore_to)
        self.menuDev.addAction(self.menuRollback_Changes.menuAction())
        self.menuDev.addSeparator()
        self.menuDev.addAction(self.actionDisable_all_modules)
        self.menuDev.addAction(self.actionExplore_to_a2_dir)
        self.menuDev.addAction(self.actionExplore_to_a2_data_dir)
        self.menuDev.addSeparator()
        self.menuDev.addAction(self.actionCreate_New_Element)
        self.menuDev.addAction(self.actionBuild_A2_Package)
        self.menuDev.addAction(self.actionSet_a2_Version)
        self.menuDev.addSeparator()
        self.menuDev.addAction(self.actionInspect_UI)
        self.menuMain.addAction(self.actionA2_settings)
        self.menuMain.addAction(self.actionRefresh_UI)
        self.menuMain.addSeparator()
        self.menuMain.addAction(self.actionReload_a2_Runtime)
        self.menuMain.addAction(self.actionLoad_a2_Runtime)
        self.menuMain.addAction(self.actionUnload_a2_Runtime)
        self.menuMain.addSeparator()
        self.menuMain.addAction(self.actionUninstall_a2)
        self.menuMain.addSeparator()
        self.menuMain.addAction(self.actionExit_a2ui)
        self.menuModule.addSeparator()
        self.menuModule.addAction(self.actionHelp_on_Module)
        self.menuModule.addAction(self.actionRevert_Settings)
        self.menuModule.addAction(self.actionExport_Settings)
        self.menuModule.addAction(self.actionImport_Settings)
        self.menuUpdates.addAction(self.action_update_a2)
        self.menuUpdates.addAction(self.action_update_packages)
        QMetaObject.connectSlotsByName(a2MainWindow)
