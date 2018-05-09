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
DEFAULT_ALPHA = 0.6
LOW_ALPHA = 0.25


class Ico(QtGui.QIcon):
    def __init__(self, ico_name, px=512, alpha=None):
        """
        :param str ico_name: Name of the icon. If present in icon library the path is
            build there. Otherwise ico_name has to be a path to the image file.
        :param int px: Prerender size of the icon image. Lower values than 512 might
            cause artifacts but might be more memory and loading speed friendly.
        :param float alpha: 0.0 to 1.0 transparency value for the icon image.
        """
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
        self._painter.end()

    @property
    def tinted(self):
        if self._tinted is None:
            self._tinted = Ico(self.path, self.px, alpha=LOW_ALPHA)

        return self._tinted


class LibIco(Ico):
    def __init__(self, name):
        super(LibIco, self).__init__(name, 512, DEFAULT_ALPHA)


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
        if self._instance:
            raise RuntimeError('Icons() has already been instanciated!\n'
                               'get it with .inst()')

        self.a2 = Ico('a2')
        self.a2close = Ico('a2x')
        self.a2reload = Ico('a2reload')
        self.a2help = Ico('a2help')
        self.autohotkey = Ico('autohotkey')
        self.github = Ico('github')

        self.button = LibIco('button')
        self.check = LibIco('check')
        self.check_circle = LibIco('check_circle')
        self.code = LibIco('code')
        self.copy = LibIco('copy')
        self.combo = LibIco('combo')
        self.clear = LibIco('clear')
        self.cloud_download = LibIco('cloud_download')
        self.cut = LibIco('cut')
        self.delete = LibIco('delete')
        self.down = LibIco('down')
        self.down_align = LibIco('down_align')
        self.down_circle = LibIco('down_circle')
        self.edit = LibIco('edit')
        self.error = LibIco('error')
        self.file_download = LibIco('file_download')
        self.folder = LibIco('folder')
        self.folder2 = LibIco('folder2')
        self.folder_add = LibIco('folder_add')
        self.group = LibIco('group')
        self.help = LibIco('help')
        self.hotkey = LibIco('keyboard')
        self.label = LibIco('label')
        self.label_plus = LibIco('label_plus')
        self.more = LibIco('more')
        self.number = LibIco('number')
        self.paste = LibIco('paste')
        self.text = LibIco('text')
        self.reload = LibIco('reload')
        self.rollback = LibIco('rollback')
        self.string = LibIco('string')
        self.up = LibIco('up')
        self.up_align = LibIco('up_align')
