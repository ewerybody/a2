import a2mod
import a2core
import a2ctrl
from PySide2 import QtGui, QtCore, QtWidgets
from a2widget import a2module_source_ui, A2ConfirmDialog, A2InputDialog

log = a2core.get_logger(__name__)
MOD_COUNT_TEXT = '%i modules, %i enabled'
UPDATE_LABEL = 'Check for Updates'
MSG_UPTODATE = 'You are Up-To-Date!'
MSG_FETCHING = 'Fetching data ...'
MSG_UPDATE_AVAILABLE = 'Update to version %s'
MSG_INSTALL_DISCLAIMER = (
    'Know about the risks of downloading and executing stuff! '
    'Install only from trusted sources! <a href="%s">read more</a>')
MSG_INSTALL_CHECK = 'I understand!'
MSG_ADD_DIALOG = ('Please provide a URL to a network location\n'
                  'or internet address to get an a2 package from:')


class ModSourceWidget(QtWidgets.QWidget):
    toggled = QtCore.Signal()
    changed = QtCore.Signal()

    def __init__(self, main, mod_source, show_enabled=False):
        super(ModSourceWidget, self).__init__()
        self.main = main
        self.mod_source = mod_source

        self.ui_body = None
        self._setup_ui(show_enabled)
        self.set_labels()

    def set_labels(self):
        self.ui.mod_count.setText(MOD_COUNT_TEXT % (self.mod_source.mod_count,
                                                    self.mod_source.enabled_count))
        self._set_body_labels()

        if self.mod_source.has_problem:
            self.ui.error_icon.setVisible(True)
            self.ui.error_icon.setToolTip(self.mod_source.get_problem_msg())
        else:
            self.ui.error_icon.setVisible(False)

    def _setup_ui(self, show_enabled):
        a2ctrl.check_ui_module(a2module_source_ui)
        self.ui = a2module_source_ui.Ui_Form()
        self.ui.setupUi(self)

        margin = 1
        self.ui.modsource_layout.setContentsMargins(margin, margin, margin, margin)

        self.ui.check.setText(self.mod_source.name)
        self.ui.check.setChecked(show_enabled)
        self.ui.check.clicked[bool].connect(self.mod_source.toggle)
        self.ui.check.clicked.connect(self.toggled.emit)

        self.ui.tool_button.clicked.connect(self._toggle_details)
        self.ui.error_icon.setIcon(a2ctrl.Icons.inst().error)

    def _set_body_labels(self):
        if self.ui_body is not None:
            self.ui_body.version_label.setText(self.mod_source.config.get('version', 'x.x.x'))
            self.ui_body.update_button.setText(UPDATE_LABEL)
            self.ui_body.maintainer_label.setText(self.mod_source.config.get('maintainer', ''))
            desc = self.mod_source.config.get('description', '')
            self.ui_body.description_label.setVisible(desc != '')
            self.ui_body.description_label.setText(desc)
            self.ui_body.local_path.value = self.mod_source.path

            url = self.mod_source.config.get('url', '')
            url_label = url
            for url_sceme in ['http://', 'https://']:
                if url_label.startswith(url_sceme):
                    url_label = url_label[len(url_sceme):]
                    break
            if url_label.startswith('www.'):
                url_label = url_label[4:]
            self.ui_body.homepage_label.setText('<a href="%s">%s</a>' % (url, url_label))

    def _toggle_details(self):
        if self.ui_body is None:
            from a2widget import a2module_source_body_ui
            a2ctrl.check_ui_module(a2module_source_body_ui)
            self.ui_body = a2module_source_body_ui.Ui_Form()
            self.ui_body.setupUi(self)
            self.ui_body.local_path.changable = False
            self.ui_body.update_button.clicked.connect(self._check_update)
            self._update_to_version = None

            self.ui_body.busy_icon = BusyIcon(self, self.main.style.get('icon_size'))
            self.ui_body.update_layout.insertWidget(1, self.ui_body.busy_icon)

            self._reset_timer = QtCore.QTimer()
            self._reset_timer.setSingleShot(True)
            self._reset_timer.timeout.connect(self._update_msg)
            self.ui_body.a2option_button.menu_called.connect(self.build_version_menu)
            self.version_menu = QtWidgets.QMenu(self)
            self.ui.modsource_layout.addWidget(self.ui_body.frame)
            self._set_body_labels()

        state = self.ui_body.frame.isVisible()
        self.ui_body.frame.setVisible(not state)
        a = [QtCore.Qt.DownArrow, QtCore.Qt.RightArrow]
        self.ui.tool_button.setArrowType(a[state])

    def set_busy(self, text=None):
        self.ui_body.busy_icon.set_busy()
        self.ui_body.update_button.setEnabled(False)
        if text:
            self.ui_body.update_button.setText(text)

    def set_idle(self):
        self.ui_body.busy_icon.set_idle()
        self.ui_body.update_button.setEnabled(True)

    def _check_update(self):
        self.set_busy(MSG_FETCHING)
        if self._update_to_version is None:
            update_check_thread = self.mod_source.get_update_checker(self.main)
            update_check_thread.data_fetched.connect(self._show_check_result)
            update_check_thread.update_error.connect(self._show_update_error)
            update_check_thread.start()
        else:
            self._change_version(self._update_to_version)

    def _show_update_finished(self):
        self.set_idle()
        self._update_msg(MSG_UPTODATE)
        self._update_to_version = None
        self.mod_source.fetch_modules()
        self.set_labels()
        self.changed.emit()

    def _show_check_result(self, remote_data):
        self.set_idle()
        remote_version = remote_data.get('version')

        if remote_version == self.mod_source.config.get('version'):
            self._update_msg(MSG_UPTODATE, a2ctrl.Icons.inst().check_circle)
        else:
            self._update_to_version = remote_version
            self.ui_body.update_button.setText(MSG_UPDATE_AVAILABLE % remote_version)
            self.ui_body.update_button.setIcon(a2ctrl.Icons.inst().cloud_download)

    def _show_update_error(self, msg):
        self.set_idle()
        self._update_msg(msg, a2ctrl.Icons.inst().error)

    def _show_update_status(self, msg):
        self.ui_body.update_button.setText(msg)

    def _update_msg(self, msg=None, icon=None):
        if msg is None:
            self._reset_timer.stop()
            self.ui_body.update_button.setText(UPDATE_LABEL)
            self.ui_body.update_button.setEnabled(True)
            self.ui_body.update_button.setIcon(QtGui.QIcon())
        else:
            self._reset_timer.start(1000)
            self.ui_body.update_button.setText(msg)
            self.ui_body.update_button.setEnabled(False)
            if icon is not None:
                self.ui_body.update_button.setIcon(icon)

    def build_version_menu(self, menu):
        icons = a2ctrl.Icons.inst()

        backup_versions = self.mod_source.get_backup_versions()
        if backup_versions:
            backup_menu = menu.addMenu('Backed up versions')
            for version in backup_versions:
                if version != self.mod_source.config.get('version'):
                    action = backup_menu.addAction(icons.rollback,
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

    def uninstall(self):
        dialog = A2ConfirmDialog(
            self.main, 'Uninstall "%s"' % self.mod_source.name,
            'This will delete the package "%s" from the module\n'
            'storage. There is NO UNDO! Beware with your own creations!')
        dialog.exec_()
        if dialog.result:
            self.mod_source.remove()
            self.changed.emit()

    def _change_version(self, version):
        self.set_busy()
        update_thread = self.mod_source.get_updater(self.main, version)
        update_thread.fetched.connect(self._show_update_finished)
        update_thread.failed.connect(self._show_update_error)
        update_thread.status.connect(self._show_update_status)
        update_thread.start()

    def rollback(self):
        to_version = self.sender().data()
        self._change_version(to_version)


class BusyIcon(QtWidgets.QLabel):
    def __init__(self, parent, size):
        super(BusyIcon, self).__init__(parent)
        self.anim_timer = QtCore.QTimer()
        self.anim_timer.setInterval(25)
        self.anim_timer.timeout.connect(self.update_rotation)
        self.icon = a2ctrl.Icons.inst().reload
        self.icon_size = size
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
    def __init__(self, main, url):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        super(AddSourceDialog, self).__init__(
            self.main, 'Add Source from URL', self.check_name, msg=MSG_ADD_DIALOG)

        self.ui.main_layout.setSpacing(self.main.style.get('spacing') * 3)
        self.h_layout = QtWidgets.QHBoxLayout()
        self.busy_icon = BusyIcon(self, self.main.style.get('icon_size'))
        self.h_layout.addWidget(self.ui.label)
        self.h_layout.addWidget(self.busy_icon)
        self.ui.main_layout.insertLayout(0, self.h_layout)

        self.checkbox = QtWidgets.QCheckBox(MSG_INSTALL_CHECK)
        self.checkbox.setVisible(False)
        self.checkbox.setChecked(True)
        self.checkbox.clicked.connect(self.check)
        self._check_understood = True
        self.ui.main_layout.insertWidget(1, self.checkbox)

        self._dialog_state = 0
        self.remote_data = None
        self.repo_url = None

        # skip input if url passed
        if url:
            self._get_remote_data(url)

    def check_name(self, name=''):
        """
        Runs on keystroke when creating new module source
        to give way to okaying creation.
        """
        if not self.checkbox.isChecked():
            return 'Tick the checkbox!'
        if not name:
            return 'Give me a URL!'
        return True

    def okay(self):
        if self._dialog_state == 0:
            self._get_remote_data()
        elif self._dialog_state == 1:
            self._install_package()
        elif self._dialog_state == 2:
            self.okayed.emit('')
            self.accept()

    def show_error(self, msg):
        log.error(msg)
        self.ui.label.setText(msg)
        self.busy_icon.set_idle()
        self.ui.a2ok_button.setText('Error')
        self.ui.a2ok_button.setEnabled(False)

    def _get_remote_data(self, url=None):
        if url is None:
            url = self.ui.text_field.text()
        else:
            self.ui.text_field.setText(url)

        result = self.check(url)
        if result is False:
            return

        self.ui.text_field.setEnabled(False)
        self.busy_icon.set_busy()
        self.ui.label.setText('fetching data ...')

        thread = a2mod.ModSourceCheckThread(self.main, check_url=url)
        thread.data_fetched.connect(self.on_data_fetched)
        thread.update_error.connect(self.show_error)
        thread.start()

    def on_data_fetched(self, data):
        self.remote_data = data
        self.busy_icon.set_idle()
        try:
            if data['name'].lower() in self.a2.module_sources:
                self.show_error('"%s" is already installed!' % data['name'])
                return

            repo_url = data.get('repo_url') or data.get('update_url') or data.get('url')
            if not repo_url:
                self.show_error('Error: No repository url found in fetched data!')
                return
            else:
                self.repo_url = repo_url

            text = 'Found: <b>{name}</b> - {version}<br><br>'.format(**data)
            desc = data.get('desc') or data.get('description')
            if desc:
                text += '"%s"\n\n' % desc
            self.ui.label.setText(text)

        except Exception as error:
            self.show_error('Error reading the fetched data!:\n%s' % error)
            return

        self.clickable_label = QtWidgets.QLabel(MSG_INSTALL_DISCLAIMER
                                            % self.a2.urls.security)
        self.clickable_label.setWordWrap(True)
        self.clickable_label.setOpenExternalLinks(True)
        self.ui.main_layout.insertWidget(1, self.clickable_label)

        self.checkbox.setChecked(False)
        self.checkbox.setVisible(True)
        self.check()
        self._dialog_state = 1
        self.resize_delayed()

    def _install_package(self):
        self.clickable_label.setVisible(False)
        self.checkbox.setVisible(False)
        self.resize_delayed()
        self.busy_icon.set_busy()

        name = self.remote_data['name']
        a2mod.create_module_source_dir(name)
        mod_source = a2mod.ModSource(self.a2, name)
        thread = a2mod.ModSourceFetchThread(
            mod_source, self.main, self.remote_data['version'], self.repo_url)

        thread.fetched.connect(self.on_install_finished)
        thread.failed.connect(self.show_error)
        thread.status.connect(self.show_status)
        thread.start()

    def show_status(self, msg):
        self.ui.label.setText(msg)

    def on_install_finished(self):
        self.busy_icon.set_idle()
        self._dialog_state = 2
        self.okay()
