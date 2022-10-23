"""
Finally an own little module all things icons.
"""
import os
from a2qt import QtGui, QtCore, QtSvg
import a2core
import a2path


log = a2core.get_logger(__name__)
ICO_PATH = None
DEFAULT_ALPHA = 0.6
LOW_ALPHA = 0.25
DEFAULT_NAME = f'{a2core.NAME}icon'
ICON_FORMATS = ['.svg', '.png', '.ico']
ICON_TYPES = [DEFAULT_NAME + ext for ext in ICON_FORMATS]
ICON_OBJ_INST_ERROR = 'Icons() has already been instanciated!\nGet it with .inst()'
_FULL_COLOR_ICONS = ('a2*', 'autohotkey', 'github')
_PLACEHOLDER_ICON = 'placeholder'
_IGNORE_ICONS = ('_ *', 'telegram_join', 'css_*', 'logo_*', _PLACEHOLDER_ICON)


class Ico(QtGui.QIcon):
    """
    Handy QIcon that:
    * regognizes names in our resources dir,
    * can directly render from svg,
    * have a tinted version if needed.
    """

    ico_path = None

    def __init__(self, ico_name, size=512, alpha=None):
        """
        :param str ico_name: Name of the icon. If present in icon library the path is
            build there. Otherwise ico_name has to be a path to the image file.
        :param int size: Pre-render size of the icon image. Lower values than 512 might
            cause artifacts but might be more memory and loading speed friendly.
        :param float alpha: 0.0 to 1.0 transparency value for the icon image.
        """
        super(Ico, self).__init__()

        self.size = size

        self._tinted = None
        self._alpha = alpha

        self._painter = None
        self._image = None

        if os.path.isfile(ico_name):
            self.path = ico_name
        else:
            if Ico.ico_path is None:
                Ico.ico_path = os.path.join(a2core.A2Obj.inst().paths.a2, 'ui', 'res', '%s.svg')
                # log.info('getting Ico.ico_path: %s', Ico.ico_path)

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
        self._image = QtGui.QImage(QtCore.QSize(self.size, self.size), QtGui.QImage.Format_ARGB32)
        self._painter = QtGui.QPainter(self._image)

        if self._alpha is not None:
            self._painter.setOpacity(self._alpha)

        renderer.render(self._painter)

    def _render(self):
        self._image = QtGui.QImage(QtCore.QSize(self.size, self.size), QtGui.QImage.Format_ARGB32)

        if self._alpha is not None:
            self._painter = QtGui.QPainter(self._image)
            image = QtGui.QImage(QtCore.QSize(self.size, self.size), QtGui.QImage.Format_ARGB32)
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
        if self._image is None or self._painter is None:
            return
        pixmap = QtGui.QPixmap.fromImage(self._image)
        self.addPixmap(pixmap)
        self._painter.end()

    @property
    def tinted(self):
        """Pass a tinted version of the same icon."""
        if self._tinted is None:
            self._tinted = Ico(self.path, self.size, alpha=LOW_ALPHA)
        return self._tinted


class Uico(Ico):
    """Ico variant with hardcoded specs.
    This is mainly for general icons with a default alpha
    that makes them fit onto random backgrounds and menus.
    """

    def __init__(self, name):
        super().__init__(name, 512, DEFAULT_ALPHA)


class _Icons:
    """
    Our load-only-once icon library object.

    For convenience this already lists all usable icons and
    for speed it just loads them up when actually needed.
    """

    # This is supposed to have many!
    # pylint: disable=too-many-instance-attributes
    _instance = None

    @staticmethod
    def inst():
        """
        :rtype: Icons
        """
        if _Icons._instance is None:
            _Icons._instance = _Icons()
        return _Icons._instance

    def __getattribute__(self, name) -> QtGui.QIcon:
        try:
            obj = super().__getattribute__(name)
        except AttributeError:
            if not name.startswith('_'):
                log.error('Icons lib got request for inexistent icon:\n  "%s"!', name)
                return Ico(_PLACEHOLDER_ICON)
            obj = Ico(_PLACEHOLDER_ICON)

        if not name.startswith('_'):
            if obj is self._ico_placeholder:
                icon = Ico(name)
            elif obj is self._uico_placeholder:
                icon = Uico(name)
            else:
                return obj
            setattr(self, name, icon)
            return icon

        return obj

    def __init__(self):
        if self._instance:
            raise RuntimeError(ICON_OBJ_INST_ERROR)
        self._ico_placeholder = QtGui.QIcon()
        self._uico_placeholder = QtGui.QIcon()

        # Icons start
        self.a2 = self._ico_placeholder
        self.a2help = self._ico_placeholder
        self.a2reload = self._ico_placeholder
        self.a2tinted = self._ico_placeholder
        self.a2x = self._ico_placeholder
        self.autohotkey = self._ico_placeholder
        self.github = self._ico_placeholder

        self.button = self._uico_placeholder
        self.check = self._uico_placeholder
        self.check_circle = self._uico_placeholder
        self.clear = self._uico_placeholder
        self.cloud_download = self._uico_placeholder
        self.code = self._uico_placeholder
        self.combo = self._uico_placeholder
        self.copy = self._uico_placeholder
        self.cut = self._uico_placeholder
        self.delete = self._uico_placeholder
        self.down = self._uico_placeholder
        self.down_align = self._uico_placeholder
        self.down_circle = self._uico_placeholder
        self.edit = self._uico_placeholder
        self.error = self._uico_placeholder
        self.file_download = self._uico_placeholder
        self.folder = self._uico_placeholder
        self.folder2 = self._uico_placeholder
        self.folder_add = self._uico_placeholder
        self.gitter = self._uico_placeholder
        self.group = self._uico_placeholder
        self.help = self._uico_placeholder
        self.keyboard = self._uico_placeholder
        self.label = self._uico_placeholder
        self.label_plus = self._uico_placeholder
        self.list_add = self._uico_placeholder
        self.locate = self._uico_placeholder
        self.more = self._uico_placeholder
        self.number = self._uico_placeholder
        self.paste = self._uico_placeholder
        self.reload = self._uico_placeholder
        self.rollback = self._uico_placeholder
        self.scope = self._uico_placeholder
        self.scope_exclude = self._uico_placeholder
        self.scope_global = self._uico_placeholder
        self.string = self._uico_placeholder
        self.telegram = self._uico_placeholder
        self.text = self._uico_placeholder
        self.up = self._uico_placeholder
        self.up_align = self._uico_placeholder
        self.volume_down = self._uico_placeholder
        self.volume_up = self._uico_placeholder
        # Icons end


Icons = _Icons.inst()


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
                fallback = Icons.a2
            current_icon = fallback

    return current_icon


def _update_icon_stub():
    """Browse the resource dir for icons and add it to this file."""
    from fnmatch import fnmatch

    with open(__file__) as file_obj:
        content = file_obj.read()

    lines = []
    full_color = set()
    lib_icons = set()
    in_icons = False

    for line in content.split('\n'):
        if line.endswith('# Icons start'):
            lines.append(line)

            in_icons = True
            res_path = os.path.abspath(os.path.join(__file__, '..', '..', 'res'))
            for icon_item in a2path.iter_types(res_path, ICON_FORMATS):
                if any(fnmatch(icon_item.base, name) for name in _IGNORE_ICONS):
                    continue

                if any(fnmatch(icon_item.base, name) for name in _FULL_COLOR_ICONS):
                    full_color.add(icon_item.base)
                else:
                    lib_icons.add(icon_item.base)

            indent = ' ' * 8
            for name in sorted(full_color):
                lines.append(f'{indent}self.{name} = self._ico_placeholder')
            lines.append('')
            for name in sorted(lib_icons):
                lines.append(f'{indent}self.{name} = self._uico_placeholder')

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
        print(
            f'Total of {num_icons} icons written into the code.'
            f'look into {new_name} to see the changes!'
        )
    else:
        print(f'Nothing changed! All {num_icons} icons already listed!')


if __name__ == '__main__':
    _update_icon_stub()
