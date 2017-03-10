"""
a2ctrl.base

@created: Aug 3, 2016
@author: eRiC
"""
import os.path
from PySide import QtGui, QtCore, QtSvg

import a2core


log = a2core.get_logger(__name__)
ICO_PATH = None


class Ico(QtGui.QIcon):
    def __init__(self, ico_name, px=512, alpha=None):
        super(Ico, self).__init__()

        self.px = px
        self._tinted = None
        self._alpha = alpha

        self._painter = None
        self._image = None

        if os.path.exists(ico_name):
            self.path = ico_name
        else:
            global ICO_PATH
            if ICO_PATH is None:
                ICO_PATH = os.path.join(a2core.A2Obj.inst().paths.a2, 'ui', 'res', '%s.svg')

            self.path = ICO_PATH % ico_name
            if not os.path.exists(self.path):
                log.error('SVG_icon: could not find path to "%s"!' % ico_name)
                return

        ext = os.path.splitext(self.path)[1].lower()
        if ext == '.svg':
            self._render_svg()
        else:
            self._render()

        self._paint()

    def _render_svg(self):
        renderer = QtSvg.QSvgRenderer(self.path)
        self._image = QtGui.QImage(QtCore.QSize(self.px, self.px), QtGui.QImage.Format_ARGB32)
        self._painter = QtGui.QPainter(self._image)

        if self._alpha is not None:
            self._painter.setOpacity(self._alpha)

        renderer.render(self._painter)

    def _render(self):
        self._image = QtGui.QImage(QtCore.QSize(self.px, self.px), QtGui.QImage.Format_ARGB32)

        if self._alpha is not None:
            self._painter = QtGui.QPainter(self._image)
            image = QtGui.QImage(QtCore.QSize(self.px, self.px), QtGui.QImage.Format_ARGB32)
            image = self._load_path_to_image(image)
            self._painter.setOpacity(self._alpha)
            self._painter.drawImage(self._image.rect(), image)
            self._painter.end()
        else:
            self._image = self._load_path_to_image(self._image)
            self._painter = QtGui.QPainter(self._image)

    def _load_path_to_image(self, image):
        image.load(self.path)
        if image.format() == QtGui.QImage.Format.Format_Indexed8:
            image = image.convertToFormat(QtGui.QImage.Format_ARGB32)
        return image

    def _paint(self):
        pixmap = QtGui.QPixmap.fromImage(self._image)
        self.addPixmap(pixmap)

    @property
    def tinted(self):
        if self._tinted is not None:
            return self._tinted

        self._tinted = Ico(self.path, self.px, alpha=0.3)
        return self._tinted


class Icons(object):
    _instance = None

    @staticmethod
    def inst():
        """
        :rtype: Icons
        """
        if Icons._instance is None:
            Icons._instance = Icons()
        return Icons._instance

    def __init__(self):
        self.a2 = Ico('a2')
        self.a2close = Ico('a2x')
        self.a2reload = Ico('a2reload')
        self.a2help = Ico('a2help')
        self.autohotkey = Ico('autohotkey')
        self.button = Ico('button')
        self.check = Ico('check')
        self.code = Ico('code')
        self.copy = Ico('copy')
        self.combo = Ico('combo')
        self.clear = Ico('clear')
        self.cut = Ico('cut')
        self.delete = Ico('delete')
        self.down = Ico('down')
        self.down_align = Ico('down_align')
        self.folder = Ico('folder')
        self.group = Ico('group')
        self.github = Ico('github')
        self.help = Ico('help')
        self.hotkey = Ico('keyboard')
        self.number = Ico('number')
        self.paste = Ico('paste')
        self.text = Ico('text')
        self.string = Ico('string')
        self.up = Ico('up')
        self.up_align = Ico('up_align')
