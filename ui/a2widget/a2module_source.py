import os

import a2mod
import a2util
import a2ctrl
from PySide import QtGui, QtCore
from a2widget import a2module_source_ui
import a2core

log = a2core.get_logger(__name__)
MOD_COUNT_TEXT = '%i modules, %i enabled'
UPDATE_LABEL = 'Check for Updates'
MSG_UPTODATE = 'You are Up-To-Date!'
MSG_NO_UPDATE_URL = 'No update-URL given!'
MSG_UPDATE_AVAILABLE = 'Update Available! %s'
MSG_UPDATE_URL_INVALID = 'Update_url Invalid'


class ModSourceWidget(QtGui.QWidget):
    toggled = QtCore.Signal()

    def __init__(self, mod_source, enabled_list):
        super(ModSourceWidget, self).__init__()
        self.mod_source = mod_source

        a2ctrl.check_ui_module(a2module_source_ui)
        self.ui = a2module_source_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.frame.setVisible(False)
        margin = 1
        self.ui.modsource_layout.setContentsMargins(margin, margin, margin, margin)

        self.ui.check.setText(mod_source.name)
        self.ui.check.setChecked(mod_source.name in enabled_list)
        self.ui.check.clicked[bool].connect(mod_source.toggle)
        self.ui.check.clicked.connect(self.toggled.emit)

        self.ui.mod_count.setText(MOD_COUNT_TEXT % (mod_source.mod_count, mod_source.enabled_count))
        self.ui.tool_button.clicked.connect(self.toggle_details)

        self.ui.version_label.setText(mod_source.config.get('version', 'x.x.x'))
        self.ui.maintainer_label.setText(mod_source.config.get('maintainer', ''))
        self.ui.local_path.changable = False
        self.ui.local_path.value = mod_source.path
        self.ui.update_button.clicked.connect(self.check_update)
        self._set_homepage_label()

        desc = mod_source.config.get('description', '')
        if not desc:
            self.ui.description_label.setVisible(False)
        else:
            self.ui.description_label.setText(desc)

        self.ui.busy_icon = BusyIcon(self)
        self.ui.update_layout.insertWidget(1, self.ui.busy_icon)

        self._reset_timer = QtCore.QTimer()
        self._reset_timer.setSingleShot(True)
        self._reset_timer.timeout.connect(self.update_msg)

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

    def toggle_details(self):
        state = self.ui.frame.isVisible()
        self.ui.frame.setVisible(not state)
        a = [QtCore.Qt.DownArrow, QtCore.Qt.RightArrow]
        self.ui.tool_button.setArrowType(a[state])

    def check_update(self):
        update_url = self.mod_source.config.get('update_url', '')
        if not update_url:
            self.update_msg(MSG_NO_UPDATE_URL)
            return

        self.ui.busy_icon.set_busy()

        # TODO: Implement this functionality in a2Mod.ModSource
        if update_url.startswith('http') or 'github.com/' in update_url:
            pass
        else:
            if os.path.exists(update_url):
                try:
                    _, base = os.path.split(update_url)
                    if base.lower() != a2mod.MOD_SOURCE_NAME:
                        update_url = os.path.join(update_url, a2mod.MOD_SOURCE_NAME)
                    remote_data = a2util.json_read(update_url)
                    remote_version = remote_data.get('version')
                    if remote_data['version'] == self.mod_source.config.get('version'):
                        self.update_msg(MSG_UPTODATE)
                    else:
                        self.update_msg(MSG_UPDATE_AVAILABLE % remote_version)
                except Exception as error:
                    self.update_msg(str(error))
            else:
                self.update_msg(MSG_UPDATE_URL_INVALID)

        self.ui.busy_icon.set_busy()

    def update_msg(self, msg=None):
        if msg is None:
            self._reset_timer.stop()
            self.ui.update_button.setText(UPDATE_LABEL)
            self.ui.update_button.setEnabled(True)
        else:
            self._reset_timer.start(1000)
            self.ui.update_button.setText(msg)
            self.ui.update_button.setEnabled(False)


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
        self._state = not self._state
        if self._state:
            self.anim_timer.start()
        else:
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
