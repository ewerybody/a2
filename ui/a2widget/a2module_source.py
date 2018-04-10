import a2ctrl
from PySide import QtGui, QtCore
from a2widget import a2module_source_ui


MOD_COUNT_TEXT = '%i modules, %i enabled'


class ModSourceWidget(QtGui.QWidget):
    toggled = QtCore.Signal()

    def __init__(self, mod_source, enabled_list):
        super(ModSourceWidget, self).__init__()
        self.mod_source = mod_source

        a2ctrl.check_ui_module(a2module_source_ui)
        self.ui = a2module_source_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.frame.setVisible(False)
        m = 1
        self.ui.modsource_layout.setContentsMargins(m, m, m, m)

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
            self.ui.update_button.setEnabled(False)
            self.ui.update_button.setText('No update-URL given!')
            return

        self.ui.busy_icon.set_busy()

        if not update_url.startswith('http'):
            pass
        else:
            pass


class BusyIcon(QtGui.QLabel):
    def __init__(self, parent):
        super(BusyIcon, self).__init__(parent)
        self._rotation = 0
        self.anim_timer = QtCore.QTimer()
        self.anim_timer.setInterval(30)
        self.anim_timer.timeout.connect(self.update_rotation)
        self.icon = a2ctrl.Icons.inst().clear
        self.setMaximumHeight(32)
        self.setMinimumHeight(32)
        self.setMaximumWidth(32)
        self.setMinimumWidth(32)
        self.setPixmap(None)
        self._state = False

    def set_busy(self):
        self._state = not self._state
        if self._state:
            self.anim_timer.start()
        else:
            self.setPixmap(None)
            self.anim_timer.stop()

    def update_rotation(self):
        self._rotation = self._rotation + 11 % 360
        pixmap = self.icon.pixmap(24, 24)
        trans = QtGui.QTransform()
        trans.rotate(self._rotation)
        pixmap = pixmap.transformed(trans)
        self.setPixmap(pixmap)
