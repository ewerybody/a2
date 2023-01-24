import time
from functools import partial

import a2util
import a2core
from a2widget import a2input_dialog
from a2widget import busy_icon
from a2qt import QtWidgets, QtCore

_DOWNLOAD_LINK = f'<center><a href=%s>Download {a2core.NAME} %s from github.com ...</a></center>'
_UPDATE_AVAILABLE = ' - <b>%s</b> <small>update available!</small>'
_CHECKING = '<small>Checking for updates ...</small>'
_CHECKED = '<small>Checked %s ago</small>'


class AboutDialog(a2input_dialog.A2ConfirmDialog):
    def __init__(self, parent):
        super().__init__(parent, f'About {a2core.NAME}')
        self.a2 = a2core.get()
        self.ui.a2cancel_button.hide()

        self.update_layout = QtWidgets.QVBoxLayout()

        self.update_button = QtWidgets.QPushButton()
        self.update_button.setText('Check for Updates')
        self.update_button.clicked.connect(self._check_updates)
        self.update_layout.addWidget(self.update_button)

        self.progress_widget = QtWidgets.QWidget(self)
        self.progress_widget.setMinimumWidth(300)
        progress_layout = QtWidgets.QHBoxLayout(self.progress_widget)
        self.busy_icon = busy_icon.BusyIcon(self)
        self.progress_bar = QtWidgets.QProgressBar(self)
        progress_layout.addWidget(self.busy_icon)
        progress_layout.addWidget(self.progress_bar)
        self.update_layout.addWidget(self.progress_widget)

        self.sublabel = QtWidgets.QLabel(self)
        self.sublabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_layout.addWidget(self.sublabel)

        self.ui.main_layout.insertLayout(1, self.update_layout)
        self.ui.main_layout.setStretch(0, 1)

        # self.setWindowFlags(a2input_dialog.FIXED_FLAGS)
        # dialog.okayed.connect(self.confirm_dialog_okayed)
        # dialog.canceled.connect(self.confirm_dialog_canceled)
        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self._draw_updates)
        self._timer.start()

        self.show()

    def _check_updates(self):
        self.setEnabled(False)
        from a2ui import UpdatesChecker

        thread = UpdatesChecker(self)
        thread.progress.connect(self._draw_updates)
        thread.finished.connect(thread.deleteLater)
        thread.start()

    def _draw_updates(self):
        lines = []
        has_update = False
        for core_item, versions in self.a2.updates['core'].items():
            line = f'<b>{core_item}</b> - {versions[0]}'

            if core_item == a2core.NAME:
                if self.a2.is_git:
                    line += ' (<i>development version</i>)'
                line = f'<h3>{line}</h3>'
                if len(versions) > 1:
                    line += _DOWNLOAD_LINK % (self.a2.urls.latest_release, versions[1])
                if self.a2.is_git:
                    line += '<br>Components:'
            else:
                if len(versions) > 1:
                    line += _UPDATE_AVAILABLE % versions[1]
                line = f'&#8226; {line}'
            lines.append(line)

        if self.a2.updates['sources']:
            lines.append('Sources:')
            for source_item, versions in self.a2.updates['sources'].items():
                line = f'&#8226; <b>{source_item}</b>'
                if versions:
                    line += f' - {versions[0]}'
                if len(versions) > 1:
                    line += _UPDATE_AVAILABLE % versions[1]
                lines.append(line)
        else:
            lines.append('No Sources to lookup updates for :(')

        self.ui.label.setText('<br>'.join(lines))

        current, total = self.a2.updates['current'], self.a2.updates['total']
        if current == total:
            self._timer.stop()
            self.update_button.show()
            self.busy_icon.set_idle()
            self.progress_widget.hide()
            time_ago = a2util.unroll_seconds(time.time() - self.a2.updates.get('checked', 0), 0)
            self.sublabel.setText(_CHECKED % time_ago)
        else:
            self.progress_widget.show()
            self.update_button.hide()
            self.busy_icon.set_busy()
            self.progress_bar.setValue(current / total * 100)
            self.sublabel.setText(_CHECKING)
        self.setEnabled(True)
        self.resize(self.width(), self.minimumSizeHint().height())
