import a2ctrl
from a2qt import QtCore, QtGui, QtWidgets



class BusyIcon(QtWidgets.QLabel):
    def __init__(self, parent, size=32):
        super().__init__(parent)
        self.anim_timer = QtCore.QTimer()
        self.anim_timer.setInterval(25)
        self.anim_timer.timeout.connect(self.update_rotation)
        self.icon = a2ctrl.Icons.reload
        self.icon_size = size
        self.rotation_speed = 22
        self.setMaximumHeight(self.icon_size)
        self.setMinimumHeight(self.icon_size)
        self.setMaximumWidth(self.icon_size)
        self.setMinimumWidth(self.icon_size)
        self._blank = QtGui.QPixmap()

        self._state = False
        self._rotation = 0

    def set_busy(self):
        self.anim_timer.start()

    def set_idle(self):
        self.setPixmap(self._blank)
        self.anim_timer.stop()

    def update_rotation(self):
        self._rotation = self._rotation + self.rotation_speed % 360
        pixmap = self.icon.pixmap(self.icon_size, self.icon_size)
        pixmap = pixmap.transformed(
            QtGui.QTransform().rotate(self._rotation), QtCore.Qt.SmoothTransformation
        )
        xoff = (pixmap.width() - self.icon_size) / 2
        yoff = (pixmap.height() - self.icon_size) / 2
        self.setPixmap(pixmap.copy(xoff, yoff, self.icon_size, self.icon_size))
