from fnmatch import fnmatch
import os

import a2path
import a2core
import a2theme
import a2ctrl.icons
from a2dev.build import CHK_MK, EX_MRK

ICON_STUB_PATH = a2ctrl.icons.__file__
ICON_FORMATS = ('.ico',)
_PLACEHOLDER_ICON = 'placeholder'
_FULL_COLOR_ICONS = ('a2*', 'autohotkey', 'github')
_IGNORE_ICONS = ('_ *', 'telegram_join', 'css_*', 'logo_*', _PLACEHOLDER_ICON)
_PLACEHOLDER_CODE = 'ico_placeholder'


def main(debug=False):
    """Browse the theme source dir for icons and add it to the icons stub."""
    a2 = a2core.get()
    print('Patching icon stub with all available files ...')
    with open(ICON_STUB_PATH) as file_obj:
        content = file_obj.read()

    lines = []
    theme_path = os.path.join(a2.paths.theme, a2theme.LIGHT_THEME)
    lib_icons = set(i.base for i in a2path.iter_types(theme_path, ICON_FORMATS))
    full_color = set(i.base for i in a2path.iter_types(a2.paths.theme, ICON_FORMATS))
    in_icons = False

    print(f'  Found {len(full_color)} full color icons')
    print(f'  Found {len(lib_icons)} lib icons')

    for line in content.split('\n'):
        if line.endswith('# Icons start'):
            lines.append(line)

            in_icons = True
            indent = ' ' * 8
            for name in sorted(full_color):
                lines.append(f'{indent}self.{name} = self._{_PLACEHOLDER_CODE}')
            lines.append('')
            for name in sorted(lib_icons):
                lines.append(f'{indent}self.{name} = self._u_{_PLACEHOLDER_CODE}')

        if line.endswith('# Icons end'):
            in_icons = False
        if in_icons:
            continue
        lines.append(line)

    new_content = '\n'.join(lines)
    num_icons = len(full_color) + len(lib_icons)
    if new_content == content:
        print(f'  {CHK_MK} Nothing changed! All {num_icons} icons already listed!')
        return

    stub_path = ICON_STUB_PATH
    if debug:
        stub_path += ' _ changed'
    with open(stub_path, 'w') as file_obj:
        file_obj.write(new_content)
    print(f'  {CHK_MK} Total of {num_icons} icons written into the stub.\n  Look into {stub_path} to see the changes!')


if __name__ == '__main__':
    main()
