"""
The unnecessarily complex example script!
"""
import os

#from siding import addons, profile, style, plugins
from siding import addons, profile

from PySide.QtGui import QAction, QKeySequence, QMainWindow, QTextEdit
from PySide.QtGui import QApplication, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    windows = []

    def __init__(self):
        super(MainWindow, self).__init__()

        # Store ourself.
        self.windows.append(self)

        # State!
        self.current_file = None

        # Editor!
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Style the editor
        #style.apply_stylesheet(self.editor, 'editor.qss')
        
        # Menus and Stuff!
        self.init_actions()
        self.init_menus()
        self.init_toolbars()
        self.init_statusbar()

        # Settings!
        self.init_settings()

        # Icons!
        self.reload_icons()
        #style.style_reloaded.connect(self.reload_icons)

        # Fancy!
        #style.enable_aero(self)
        self.update_title()

        # Now, for some plugins.
#        plugins.run_signal('new_window', self)

    ##### Action Icons! #######################################################

    def reload_icons(self):
        #self.setWindowIcon(style.icon('application'))
        pass
#         a = self.actions
#         for key in a.keys():
#             a[key].setIcon(style.icon(key.lower()))

    ##### Actions! ############################################################

    def init_actions(self):
        self.actions = a = {}

        ##### File Menu #######################################################

        a['document-new'] = QAction("&New", self, shortcut=QKeySequence.New,
                        statusTip="Create a new file.",
                        triggered=self.action_new)

        a['document-open'] = QAction("&Open", self, shortcut=QKeySequence.Open,
                        statusTip="Open an existing file.",
                        triggered=self.action_open)

        a['document-save'] = QAction("&Save", self, shortcut=QKeySequence.Save,
                        statusTip="Save the document to disk.",
                        triggered=self.action_save)

        a['application-exit'] = QAction("E&xit", self,
                        statusTip="Exit the application.",
                        triggered=self.close)

        ##### Edit Menu #######################################################

        a['edit-cut'] = QAction("Cu&t", self, shortcut=QKeySequence.Cut,
                        triggered=self.editor.cut)

        a['edit-copy'] = QAction("&Copy", self, shortcut=QKeySequence.Copy,
                        triggered=self.editor.copy)

        a['edit-paste'] = QAction("&Paste", self, shortcut=QKeySequence.Paste,
                        triggered=self.editor.paste)

        a['edit-cut'].setEnabled(False)
        a['edit-copy'].setEnabled(False)

        self.editor.copyAvailable.connect(a['edit-cut'].setEnabled)
        self.editor.copyAvailable.connect(a['edit-copy'].setEnabled)

        ##### Tool Menu #######################################################

        # This is the fun part.
        a['addon-manager'] = QAction("&Add-ons", self, shortcut="Ctrl+Shift+A",
                                statusTip="Display the Add-ons manager.",
                                triggered=addons.show)

#         a['view-refresh'] = QAction("&Reload Style", self,
#                                 shortcut="Ctrl+Shift+R",
#                                 statusTip="Reload the style.",
#                                 triggered=style.reload)

    ##### Menus! ##############################################################

    def init_menus(self):
        self.menuBar().clear()
        a = self.actions

        file = self.menuBar().addMenu("&File")
        file.addAction(a['document-new'])
        file.addAction(a['document-open'])
        file.addAction(a['document-save'])
        file.addSeparator()
        file.addAction(a['application-exit'])

        edit = self.menuBar().addMenu("&Edit")
        edit.addAction(a['edit-cut'])
        edit.addAction(a['edit-copy'])
        edit.addAction(a['edit-paste'])

        tools = self.menuBar().addMenu("&Tools")
        tools.addAction(a['addon-manager'])
        #tools.addAction(a['view-refresh'])

    ##### Explosions! #########################################################

    ##### Toolbars! ###########################################################

    def init_toolbars(self):
        a = self.actions

        file = self.addToolBar("File")
        file.setObjectName('filebar')
        file.addAction(a['document-new'])
        file.addAction(a['document-open'])
        file.addAction(a['document-save'])

        edit = self.addToolBar("Edit")
        edit.setObjectName('editbar')
        edit.addAction(a['edit-cut'])
        edit.addAction(a['edit-copy'])
        edit.addAction(a['edit-paste'])

        tools = self.addToolBar("Tools")
        tools.setObjectName('toolsbar')
        tools.addAction(a['addon-manager'])
        #tools.addAction(a['view-refresh'])

    ##### Statusbars! #########################################################

    def init_statusbar(self):
        self.statusBar().showMessage("Ready.")

    ##### Settings! ###########################################################

    def init_settings(self):
        self.restoreGeometry(profile.get("geometry"))
        self.restoreState(profile.get("state"))

    def save_settings(self):
        profile.set("geometry", self.saveGeometry())
        profile.set("state", self.saveState())

    ##### Actual Actions! #####################################################

    def update_title(self):
        if self.current_file:
            title = os.path.basename(self.current_file)
        else:
            title = "Untitled"
        self.setWindowTitle("%s - %s" % (title,
                QApplication.instance().applicationName()))

    def action_new(self):
        if self.try_save():
            self.editor.clear()
            self.current_file = None
            self.update_title()

    def action_open(self):
        if self.try_save():
            fn = QFileDialog.getOpenFileName(self)[0]
            if not fn:
                return

            self.do_open(fn)

    def do_open(self, fn):
        with open(fn, 'r') as f:
            content = f.read()

        self.editor.setPlainText(content)
        self.current_file = fn
        self.update_title()

    def action_save(self):
        if not self.editor.document().isModified():
            return

        if not self.current_file:
            self.current_file = QFileDialog.getSaveFileName(self)[0]
            self.update_title()

        if not self.current_file:
            return

        with open(self.current_file, 'w') as f:
            f.write(self.editor.toPlainText())
        self.editor.document().setModified(False)

    ##### Adventure! ##########################################################

    def try_save(self):
        if self.editor.document().isModified():
            ret = QMessageBox.warning(self, "Blah Blah Blah",
                    "That's an awfully nice modified document you've got there"
                    ". It'd be a shame if anything... happened to it. Catch "
                    "my drift?",
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                    )
            if ret == QMessageBox.Save:
                self.action_save()

            elif ret == QMessageBox.Cancel:
                return False

        return True

    def showRaise(self):
        """ Show and raise the window. """
#         self.show()
#         self.raise_()
#         self.setFocus()
        self.activateWindow()
        if self.isMinimized():
            self.showNormal()

    def closeEvent(self, event):
        if self.try_save():
            self.save_settings()

            if self in self.windows:
                self.windows.remove(self)

#            plugins.run_signal('close_window', self)

            event.accept()
        else:
            event.ignore()
