from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2module_list import A2ModuleList
from a2widget.a2module_view import A2ModuleView


class Ui_a2MainWindow:
    actionExport_Settings: QAction
    actionImport_Settings: QAction
    actionAbout_a2: QAction
    actionEdit_module: QAction
    actionDisable_all_modules: QAction
    actionExplore_to: QAction
    actionAbout_Autohotkey: QAction
    actionExplore_to_a2_dir: QAction
    actionA2_settings: QAction
    actionExit_a2ui: QAction
    actionRefresh_UI: QAction
    actionReport_Issue: QAction
    actionNew_Module_Dialog: QAction
    actionBuild_A2_Package: QAction
    actionCreate_New_Element: QAction
    actionHelp_on_Module: QAction
    actionRevert_Settings: QAction
    actionReload_a2_Runtime: QAction
    actionUnload_a2_Runtime: QAction
    actionLoad_a2_Runtime: QAction
    actionExplore_to_a2_data_dir: QAction
    action_report_bug: QAction
    action_report_sugg: QAction
    actionUninstall_a2: QAction
    centralwidget: QWidget
    verticalLayout: QVBoxLayout
    splitter: QSplitter
    module_list: A2ModuleList
    module_view: A2ModuleView
    menubar: QMenuBar
    menuHelp: QMenu
    menuDev: QMenu
    menuRollback_Changes: QMenu
    menuMain: QMenu
    menuModule: QMenu

    def setupUi(self, a2MainWindow: QMainWindow) -> None: ...
