from a2qt.QtCore import *
from a2qt.QtGui import *
from a2qt.QtWidgets import *

from a2widget.a2module_list import A2ModuleList
from a2widget.a2module_view import A2ModuleView


class Ui_a2MainWindow:
    def setupUi(self, a2MainWindow: QMainWindow):
        self.actionAbout_a2 = QAction(a2MainWindow)
        self.actionEdit_module = QAction(a2MainWindow)
        self.actionDisable_all_modules = QAction(a2MainWindow)
        self.actionExplore_to = QAction(a2MainWindow)
        self.actionAbout_Autohotkey = QAction(a2MainWindow)
        self.actionExplore_to_a2_dir = QAction(a2MainWindow)
        self.actionA2_settings = QAction(a2MainWindow)
        self.actionExit_a2ui = QAction(a2MainWindow)
        self.actionRefresh_UI = QAction(a2MainWindow)
        self.actionReport_Issue = QAction(a2MainWindow)
        self.actionNew_Module_Dialog = QAction(a2MainWindow)
        self.actionBuild_A2_Package = QAction(a2MainWindow)
        self.actionCreate_New_Element = QAction(a2MainWindow)
        self.actionHelp_on_Module = QAction(a2MainWindow)
        self.actionRevert_Settings = QAction(a2MainWindow)
        self.actionReload_a2_Runtime = QAction(a2MainWindow)
        self.actionUnload_a2_Runtime = QAction(a2MainWindow)
        self.actionLoad_a2_Runtime = QAction(a2MainWindow)
        self.actionExplore_to_a2_data_dir = QAction(a2MainWindow)
        self.action_report_bug = QAction(a2MainWindow)
        self.action_report_sugg = QAction(a2MainWindow)
        self.actionUninstall_a2 = QAction(a2MainWindow)
        self.centralwidget = QWidget(a2MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.splitter = QSplitter(self.centralwidget)
        self.module_list = A2ModuleList(self.splitter)
        self.module_view = A2ModuleView(self.splitter)
        self.menubar = QMenuBar(a2MainWindow)
        self.menuHelp = QMenu(self.menubar)
        self.menuDev = QMenu(self.menubar)
        self.menuRollback_Changes = QMenu(self.menuDev)
        self.menuMain = QMenu(self.menubar)
        self.menuModule = QMenu(self.menubar)