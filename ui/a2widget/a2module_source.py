import a2core
import a2ctrl
from PySide import QtGui, QtCore
from a2widget import a2module_source_ui, A2ConfirmDialog, A2InputDialog

log = a2core.get_logger(__name__)
MOD_COUNT_TEXT = '%i modules, %i enabled'
UPDATE_LABEL = 'Check for Updates'
MSG_UPTODATE = 'You are Up-To-Date!'
MSG_UPDATE_AVAILABLE = 'Update to version %s'


class ModSourceWidget(QtGui.QWidget):
    toggled = QtCore.Signal()
    changed = QtCore.Signal()

    def __init__(self, parent, mod_source, show_enabled=False):
        super(ModSourceWidget, self).__init__()
        self.parent = parent
        self.mod_source = mod_source

        self._setup_ui(show_enabled)
        self.set_labels()

    def set_labels(self):
        self.ui.mod_count.setText(MOD_COUNT_TEXT % (self.mod_source.mod_count,
                                                    self.mod_source.enabled_count))
        self.ui.version_label.setText(self.mod_source.config.get('version', 'x.x.x'))
        self.ui.maintainer_label.setText(self.mod_source.config.get('maintainer', ''))
        self._set_homepage_label()

        desc = self.mod_source.config.get('description', '')
        self.ui.description_label.setVisible(desc != '')
        self.ui.description_label.setText(desc)
        self.ui.local_path.value = self.mod_source.path

    def _setup_ui(self, show_enabled):
        a2ctrl.check_ui_module(a2module_source_ui)
        self.ui = a2module_source_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.frame.setVisible(False)
        margin = 1
        self.ui.modsource_layout.setContentsMargins(margin, margin, margin, margin)

        self.ui.check.setText(self.mod_source.name)
        self.ui.check.setChecked(show_enabled)
        self.ui.check.clicked[bool].connect(self.mod_source.toggle)
        self.ui.check.clicked.connect(self.toggled.emit)

        self.ui.tool_button.clicked.connect(self._toggle_details)
        self.ui.local_path.changable = False
        self.ui.update_button.clicked.connect(self._check_update)
        self._update_to_version = None

        self.ui.busy_icon = BusyIcon(self)
        self.ui.update_layout.insertWidget(1, self.ui.busy_icon)

        self._reset_timer = QtCore.QTimer()
        self._reset_timer.setSingleShot(True)
        self._reset_timer.timeout.connect(self._update_msg)
        self.ui.version_tool_button.clicked.connect(self.build_version_menu)
        self.version_menu = QtGui.QMenu(self)

    def _set_homepage_label(self):
        url = self.mod_source.config.get('url', '')
        url_label = url
        for url_sceme in ['http://', 'https://']:
            if url_label.startswith(url_sceme):
                url_label = url_label[len(url_sceme):]
                break
        if url_label.startswith('www.'):
            url_label = url_label[4:]
        self.ui.homepage_label.setText('<a href="%s">%s</a>' % (url, url_label))

    def _toggle_details(self):
        state = self.ui.frame.isVisible()
        self.ui.frame.setVisible(not state)
        a = [QtCore.Qt.DownArrow, QtCore.Qt.RightArrow]
        self.ui.tool_button.setArrowType(a[state])

    def _check_update(self):
        self.ui.busy_icon.set_busy()
        if self._update_to_version is None:
            update_check_thread = self.mod_source.get_update_checker(self.parent)
            update_check_thread.is_uptodate.connect(self._show_uptodate)
            update_check_thread.update_available.connect(self._show_update_available)
            update_check_thread.update_error.connect(self._show_update_error)
            update_check_thread.start()
        else:
            self._change_version(self._update_to_version)

    def _show_uptodate(self):
        self._update_msg(MSG_UPTODATE)
        self.ui.busy_icon.set_idle()

    def _show_update_finished(self):
        self._update_msg(MSG_UPTODATE)
        self._update_to_version = None
        self.ui.busy_icon.set_idle()
        self.mod_source.fetch_modules()
        self.set_labels()
        self.changed.emit()

    def _show_update_available(self, version):
        self._update_to_version = version
        self.ui.update_button.setText(MSG_UPDATE_AVAILABLE % version)
        self.ui.busy_icon.set_idle()

    def _show_update_error(self, msg):
        self._update_msg(msg)
        self.ui.busy_icon.set_idle()

    def _show_update_status(self, msg):
        self.ui.update_button.setText(msg)

    def _update_msg(self, msg=None):
        if msg is None:
            self._reset_timer.stop()
            self.ui.update_button.setText(UPDATE_LABEL)
            self.ui.update_button.setEnabled(True)
        else:
            self._reset_timer.start(1000)
            self.ui.update_button.setText(msg)
            self.ui.update_button.setEnabled(False)

    def build_version_menu(self):
        menu = self.version_menu
        icons = a2ctrl.Icons.inst()

        menu.clear()
        backup_versions = self.mod_source.get_backup_versions()
        if backup_versions:
            backup_menu = menu.addMenu('Backed up versions')
            for version in backup_versions:
                if version != self.mod_source.config.get('version'):
                    action = backup_menu.addAction(icons.file_download,
                                                   version, self.rollback)
                    action.setData(version)

            backup_menu.addSeparator()
            backup_menu.addAction(icons.delete, 'Remove backups',
                                  self.mod_source.remove_backups)
        else:
            action = menu.addAction('No backed up verions!')
            action.setEnabled(False)
        menu.addSeparator()
        menu.addAction(icons.delete, 'Uninstall "%s"' % self.mod_source.name,
                       self.uninstall)

        menu.popup(self.cursor().pos())

    def uninstall(self):
        dialog = A2ConfirmDialog(
            self.parent, 'Uninstall "%s"' % self.mod_source.name,
            'This will delete the package "%s" from the module\n'
            'storage. There is NO UNDO! Beware with your own creations!')
        dialog.exec_()
        if dialog.result:
            self.mod_source.remove()
            self.changed.emit()

    def _change_version(self, version):
        self.ui.busy_icon.set_busy()
        update_thread = self.mod_source.get_updater(version, self.parent)
        update_thread.finished.connect(self._show_update_finished)
        update_thread.failed.connect(self._show_update_error)
        update_thread.status.connect(self._show_update_status)
        update_thread.start()

    def rollback(self):
        to_version = self.sender().data()
        self._change_version(to_version)


class BusyIcon(QtGui.QLabel):
    def __init__(self, parent):
        super(BusyIcon, self).__init__(parent)
        self.anim_timer = QtCore.QTimer()
        self.anim_timer.setInterval(25)
        self.anim_timer.timeout.connect(self.update_rotation)
        self.icon = a2ctrl.Icons.inst().a2reload
        self.icon_size = 24
        self.rotation_speed = 22
        self.setMaximumHeight(self.icon_size)
        self.setMinimumHeight(self.icon_size)
        self.setMaximumWidth(self.icon_size)
        self.setMinimumWidth(self.icon_size)
        self.setPixmap(None)

        self._state = False
        self._rotation = 0

    def set_busy(self):
        self.anim_timer.start()

    def set_idle(self):
        self.setPixmap(None)
        self.anim_timer.stop()

    def update_rotation(self):
        self._rotation = self._rotation + self.rotation_speed % 360
        pixmap = self.icon.pixmap(self.icon_size, self.icon_size)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self._rotation),
                                    QtCore.Qt.SmoothTransformation)
        xoff = (pixmap.width() - self.icon_size) / 2
        yoff = (pixmap.height() - self.icon_size) / 2
        self.setPixmap(pixmap.copy(xoff, yoff, self.icon_size, self.icon_size))


class AddSourceDialog(A2InputDialog):
    def __init__(self, main):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.source_names = [m.lower() for m in self.a2.module_sources]
        super(AddSourceDialog, self).__init__(
            self.main, 'Add Source from URL', self.check_name,
            msg=('Please provide a URL to a network location\n'
                 'or internet address to get an a2 package from:'))

    def check_name(self, name):
        """
        Runs on keystroke when creating new module source
        to give way to okaying creation.
        """
        if not name:
            return 'Give me a URL!'
        return True
