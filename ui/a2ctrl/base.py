"""
a2ctrl.base

@created: Aug 3, 2016
@author: eRiC
"""
from os.path import exists, join
from PySide import QtGui, QtCore, QtSvg

import a2core


log = a2core.get_logger(__name__)
ICO_PATH = None


class Ico(QtGui.QIcon):
    def __init__(self, ico_name, px=512, scale=1.0, color=None):
        super(Ico, self).__init__()
        if exists(ico_name):
            self.path = ico_name
        else:
            global ICO_PATH
            if ICO_PATH is None:
                ICO_PATH = join(a2core.A2Obj.inst().paths.a2, 'ui', 'res', '%s.svg')
            self.path = ICO_PATH % ico_name
            if not exists(self.path):
                log.error('SVG_icon: could not find path to "%s"!' % ico_name)
                return

        renderer = QtSvg.QSvgRenderer(self.path)
        image = QtGui.QImage(QtCore.QSize(px, px), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)

        if scale != 1.0:
            t = (px / 2) * (1 - scale)
            painter.translate(t, t)
            painter.scale(scale, scale)

        renderer.render(painter)

        if color:
            if isinstance(color, (int, float)):
                color = [int(color)] * 3
            if isinstance(color, (tuple, list)):
                color = QtGui.QColor(color[0], color[1], color[2])
            if isinstance(color, QtGui.QColor):
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
                painter.fillRect(image.rect(), color)
            else:
                log.error('Cannot use color: "%s"' % str(color))

        pixmap = QtGui.QPixmap.fromImage(image)
        self.addPixmap(pixmap)
        painter.end()


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
