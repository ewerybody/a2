import os
import time
import a2core
import a2path

from PySide2 import QtGui, QtCore, QtSvg


log = a2core.get_logger(__name__)
ICO_PATH = None
DEFAULT_ALPHA = 0.6
LOW_ALPHA = 0.25
DEFAULT_NAME = f'{a2core.NAME}icon'
ICON_FORMATS = ['.svg', '.png', '.ico']
ICON_TYPES = [DEFAULT_NAME + ext for ext in ICON_FORMATS]
ICON_OBJ_INST_ERROR = 'Icons() has already been instanciated!\nGet it with .inst()'


class Ico(QtGui.QIcon):
    ico_path = None

    def __init__(self, ico_name, px=512, alpha=None):
        """
        :param str ico_name: Name of the icon. If present in icon library the path is
            build there. Otherwise ico_name has to be a path to the image file.
        :param int px: Pre-render size of the icon image. Lower values than 512 might
            cause artifacts but might be more memory and loading speed friendly.
        :param float alpha: 0.0 to 1.0 transparency value for the icon image.
        """
        super(Ico, self).__init__()

        self.px = px

        self._tinted = None
        self._alpha = alpha

        self._painter = None
        self._image = None

        if os.path.isfile(ico_name):
            self.path = ico_name
        else:
            if Ico.ico_path is None:
                Ico.ico_path = os.path.join(a2core.A2Obj.inst().paths.a2, 'ui', 'res', '%s.svg')
                log.info('getting Ico.ico_path: %s', Ico.ico_path)

            self.path = Ico.ico_path % ico_name
            if not os.path.isfile(self.path):
                log.error('SVG_icon: could not find path to "%s"!', ico_name)
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
        """Pass a tinted version of the same icon."""
        if self._tinted is None:
            self._tinted = Ico(self.path, self.px, alpha=LOW_ALPHA)
        return self._tinted


class LibIco(Ico):
    """Ico variant with hardcoded specs."""
    def __init__(self, name):
        super(LibIco, self).__init__(name, 512, DEFAULT_ALPHA)


class Icons(object):
    # This is supposed to have many!
    # pylint: disable=too-many-instance-attributes
    """Our load-only-once icon library object."""
    _instance = None

    @staticmethod
    def inst():
        """
        :rtype: Icons
        """
        if Icons._instance is None:
            Icons._instance = Icons()
        return Icons._instance

    def __getattribute__(self, name):
        try:
            obj = super(Icons, self).__getattribute__(name)
        except AttributeError:
            obj, name
        if not name.startswith('_'):
            if isinstance(obj, bool):
                obj, name
            return obj
        else:
            return obj

    def __init__(self):
        if self._instance:
            raise RuntimeError(ICON_OBJ_INST_ERROR)
        t0 = time.time()

        # Icons start
        self.a2 = Ico('a2')
        self.a2help = Ico('a2help')
        self.a2reload = Ico('a2reload')
        self.a2tinted = Ico('a2tinted')
        self.a2x = Ico('a2x')
        self.autohotkey = Ico('autohotkey')
        self.github = Ico('github')

        self.button = LibIco('button')
        self.check = LibIco('check')
        self.check_circle = LibIco('check_circle')
        self.clear = LibIco('clear')
        self.cloud_download = LibIco('cloud_download')
        self.code = LibIco('code')
        self.combo = LibIco('combo')
        self.copy = LibIco('copy')
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
        self.keyboard = LibIco('keyboard')
        self.label = LibIco('label')
        self.label_plus = LibIco('label_plus')
        self.list_add = LibIco('list_add')
        self.locate = LibIco('locate')
        self.more = LibIco('more')
        self.number = LibIco('number')
        self.paste = LibIco('paste')
        self.reload = LibIco('reload')
        self.rollback = LibIco('rollback')
        self.scope = LibIco('scope')
        self.scope_exclude = LibIco('scope_exclude')
        self.scope_global = LibIco('scope_global')
        self.string = LibIco('string')
        self.text = LibIco('text')
        self.up = LibIco('up')
        self.up_align = LibIco('up_align')
        # Icons end
        print('%s took %.3fs' % ('Icons', time.time() - t0))


def get(current_icon, folder, fallback=None):
    """Find an icon path or fallback."""
    if current_icon is None or not os.path.isfile(current_icon.path):
        icon_path = ''
        for item in a2path.iter_files(folder):
            if item.name in ICON_TYPES:
                icon_path = item.path
                break

        if icon_path:
            current_icon = Ico(icon_path)
        else:
            if fallback is None:
                fallback = Icons.inst().a2
            current_icon = fallback

    return current_icon


def _update_icon_stub():
    from fnmatch import fnmatch
    with open(__file__) as file_obj:
        content = file_obj.read()

    lines = []
    full_color_names = ('a2*', 'autohotkey', 'github')
    ignore_these = ('telegram_join', 'css_*', 'logo_*')
    full_color = set()
    lib_icons = set()
    in_icons = False

    for line in content.split('\n'):
        if line.endswith('# Icons start'):
            lines.append(line)

            in_icons = True
            res_path = os.path.abspath(os.path.join(__file__, '..', '..', 'res'))
            for icon_item in a2path.iter_types(res_path, ICON_FORMATS):
                if any(fnmatch(icon_item.base, name) for name in ignore_these):
                    continue

                if any(fnmatch(icon_item.base, name) for name in full_color_names):
                    full_color.add(icon_item.base)
                else:
                    lib_icons.add(icon_item.base)

            indent = ' ' * 8
            for name in sorted(full_color):
                lines.append(f"{indent}self.{name} = Ico('{name}')")
            lines.append('')
            for name in sorted(lib_icons):
                lines.append(f"{indent}self.{name} = LibIco('{name}')")

        if line.endswith('# Icons end'):
            in_icons = False
        if in_icons:
            continue
        lines.append(line)

    new_content = '\n'.join(lines)
    num_icons = len(full_color) + len(lib_icons)
    if new_content != content:
        new_name = __file__ + ' _ changed'
        with open(new_name, 'w') as file_obj:
            file_obj.write(new_content)
        print(f'Total of {num_icons} icons written into the code.'
              f'look into {new_name} to see the changes!')
    else:
        print(f'Nothing changed! All {num_icons} icons already listed!')


if __name__ == "__main__":
    _update_icon_stub()
