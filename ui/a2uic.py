"""
Handle Qt Designer file updating, compilation and patching.
"""
import os
import sys
from importlib import reload

import a2core
from a2qt import QtCore, QtGui, QtWidgets, QtSvg

log = a2core.get_logger(__name__)

ROOT_PATH = os.path.abspath(os.path.join(a2core.__file__, '..', '..'))
UI_FILE_SUFFIX = '_ui'
PYSIDE_REPLACE = 'a2qt'
OLDSCHOOL_CLASS = '(object):\n'
TRANSLATE = '(QCoreApplication.translate('
LINE_LEN = 95
QMEMBERS = {}
MEMBERSQ = {}


def check_module(module, force=False):
    """
    Recompile a ui xml file to Python if out-of-date.

    :param module module: Module object to check.
    """
    if not a2core.is_dev_mode():
        return

    if getattr(sys, 'frozen', False):
        # log.info('frozen! no need to compile %s' % module)
        return

    py_file_path = module.__file__
    ui_file_path = get_ui_file_path(module.__file__)
    if not ui_file_path or not os.path.isfile(ui_file_path):
        return

    time_diff = os.path.getmtime(py_file_path) - os.path.getmtime(ui_file_path)
    if not force and os.path.getsize(py_file_path) and time_diff > 0:
        return

    log.debug('%s needs compile! (age: %is)', ui_file_path, time_diff)
    call_uic(ui_file_path, py_file_path)

    UIPatcher(ui_file_path, py_file_path)

    reload(module)


def get_ui_file_path(py_file_path):
    """Get the `.ui` file path from an already compiled `..._ui.py` file.
    """
    dir_path, py_base = os.path.split(py_file_path)
    ui_name = os.path.splitext(py_base)[0]

    if ui_name.endswith(UI_FILE_SUFFIX):
        ui_base = ui_name[: -len(UI_FILE_SUFFIX)] + '.ui'
    else:
        ui_base = _get_ui_basename_from_header(py_file_path)

    if not ui_base:
        raise RuntimeError(
            f'Could not get source ui file from module:\n {py_file_path}\n  '
            'Not a ui file module??!'
        )

    return os.path.join(dir_path, ui_base)


def call_uic(ui_file_path, py_file_path):
    """Call the original Qt ui compiler in Python mode in proper path project
    relation.
    """
    # Newer uic seems to just put the basename in the header... however.
    # Make paths in compiled files project related, not from current user.
    curr_cwd = os.getcwd()
    ui_relative = os.path.relpath(ui_file_path, ROOT_PATH)
    os.chdir(ROOT_PATH)

    import subprocess
    import a2qt

    uic_path = os.path.join(a2qt.QT_PATH, 'uic.exe')
    subprocess.call([uic_path, '-g', 'python', ui_relative, '-o', py_file_path])

    os.chdir(curr_cwd)


class UIPatcher:
    """
    Patch compiled ui file to fix a couple of problems there are with
    the default uic executable. See #219. Done:
    [x] make use of a2qt wrapper instead of PySideX
    [x] remove main-obj resizes (!!!!!)
    [x] make a proper doc-string instead of comments block
    [x] remove #if/#endif comments
    [x] remove # setupUi and # retranslateUi comments
    [x] remove retranslateUi and its call if empty
    [x] remove unneeded empty lines
    [x] make it class Name: instead of oldschool class Name(object):
    [x] get rid of broad * imports
    [x] `"` and `u"` to `'` (make it black/brunette compliant)
        (I'd rather leave this to black/brunette itself, but maybe in a separate
        (process that auto-checks for updated ui-files.)
    """
    def __init__(self, uiname, py_file_path):
        self.uiname = uiname
        self.py_file_path = py_file_path
        _get_qmembers()

        with open(py_file_path, encoding='utf8') as pyfobj:
            self.lines = pyfobj.readlines()

        self.doc_block = self._fix_doc_string()
        self.imports_block = self._fix_imports_block()
        self.classes_start = self._fix_classes_block()
        self.obj_name = self._get_obj_name()
        self.translate_id = f'{TRANSLATE}"{self.obj_name}", '
        self._id_len = len(self.translate_id)
        self.translate_fix = f"{TRANSLATE}'{self.obj_name}', "

        self.submods_used: dict[str, dict | set] = {}
        self.translate_lines: list[None | int] = [None, None]
        self._fix_main_block()
        self._fix_translate_block()

        new_lines = self._assemble_new_lines()
        with open(py_file_path, 'w', encoding='utf8') as pyfobj:
            pyfobj.write(''.join(new_lines))

    def _fix_doc_string(self):
        mod_doc_block = []
        for i, line in enumerate(self.lines):
            if mod_doc_block and not line.strip():
                mod_doc_block.append(i)
                break
            if line.startswith('##') and not mod_doc_block:
                mod_doc_block = [i]
        return mod_doc_block

    def _fix_imports_block(self):
        pyside_import_lines = []
        start = self.doc_block[1]
        submod_lines = {}
        sub_module = ''
        for i, line in enumerate(self.lines[start:], start):
            # finish when collected and next line is empty
            if pyside_import_lines and not line.strip():
                break

            if line.startswith('from PySide'):
                parts = line.split()
                dot_pos = parts[1].find('.')
                if dot_pos == -1:
                    raise RuntimeError('Patching compiled ui failed on line %i:\n  %s' % (i, line))

                sub_module = parts[1][dot_pos + 1 :]
                parts[1] = PYSIDE_REPLACE + '.' + sub_module
                self.lines[i] = ' '.join(parts) + '\n'
                pyside_import_lines.append(i)
                submod_lines[sub_module] = [i]

            elif sub_module:
                submod_lines[sub_module].append(i)
                pyside_import_lines.append(i)

        pyside_import_lines[:] = [min(pyside_import_lines), max(pyside_import_lines)]

        if not all(mod in globals() for mod in submod_lines):
            raise RuntimeError('Not all Qt Submodules loaded!')
        return pyside_import_lines

    def _fix_classes_block(self):
        class_block_start = None
        start = self.imports_block[-1] + 1
        for i, line in enumerate(self.lines[start:], start):
            if class_block_start is None and line.startswith('class '):
                class_block_start = i
                if line.endswith(OLDSCHOOL_CLASS):
                    self.lines[i] = line[: -len(OLDSCHOOL_CLASS)] + ':\n'
                break

        if class_block_start is None:
            raise RuntimeError('class_block_start was not found!')
        return class_block_start

    def _get_obj_name(self):
        parts = self.lines[self.classes_start + 1].split()
        assert parts[0] == 'def'
        assert parts[1] == 'setupUi(self,'
        assert parts[2].endswith('):')
        return parts[2][:-2]

    def _fix_main_block(self):
        resize_removed = False
        for i, _line in enumerate(self.lines[self.classes_start + 1 :], self.classes_start + 1):
            line = _line.strip()
            if not line:
                self.lines[i] = ''
            # Remove the resize. All our uis are dynamically sized.
            elif not resize_removed and line.startswith(f'{self.obj_name}.resize('):
                self.lines[i] = ''
                resize_removed = True
            # remove comments
            elif line.startswith('#'):
                self.lines[i] = ''

            # to remove translation func if empty
            elif line.startswith('self.retranslateUi('):
                self.translate_lines[1] = i
            elif line.startswith('def retranslateUi(self, '):
                self.translate_lines[0] = i

            self._gather_sub_modules(line)
            self._fix_string_quotes(line, i)

    def _fix_translate_block(self):
        """
        look for unnecessary `pass` at the end of translate block
        """
        def_line, call_line = self.translate_lines
        if def_line is None:
            return

        for i in range(def_line + 1, len(self.lines)):
            line = self.lines[i].strip()
            if not line:
                continue
            if line == 'pass' and call_line is not None:
                self.lines[def_line] = ''
                self.lines[i] = ''
                self.lines[call_line] = ''
                return

        def_line += 1
        for i, _line in enumerate(self.lines[def_line:], def_line):
            if _line.startswith('    def '):
                break
            if _line.strip() == 'pass':
                self.lines[i] = ''

    def _gather_sub_modules(self, line):
        if not line:
            return
        for word, mod in MEMBERSQ.items():
            if word in line:
                if line[line.find(word) + len(word)] in '(.':
                    self.submods_used.setdefault(mod, set()).add(word)
                else:
                    log.debug('Word "%s" found in line but not handled!\n> %s', word, line)

    def _fix_string_quotes(self, line, i):
        if not line or not self.lines[i]:
            return
        set_pos = self.lines[i].find('.set')
        if set_pos == -1:
            return

        line = self.lines[i]
        translate_pos = line.find(self.translate_id, set_pos)
        if translate_pos == -1:
            open_pos = line.find('(u"', set_pos)
            command = line[set_pos + 4:open_pos]
            end = '")\n'

        else:
            open_pos = line.find(' u"', translate_pos)
            command = line[set_pos + 4:translate_pos]
            line = line[:translate_pos] + self.translate_fix + line[translate_pos + self._id_len:]
            self.lines[i] = line
            end = '", None))\n'

        if open_pos == -1:
            return

        linebreak = '\\n"\n'
        if line.endswith(linebreak):
            for ni, next_line in enumerate(self.lines[i + 1:], i + 1):
                if not next_line.startswith('"'):
                    break
                if self.lines[i].endswith(linebreak):
                    line = self.lines[i][:-len(linebreak) + 2] + next_line[1:]
                    self.lines[i] = line
                    self.lines[ni] = ''
                else:
                    break

        if not line.endswith(end):
            return

        content = line[open_pos + 3: -len(end)]
        if not content:
            log.error('Setting %s to empty string in line %i!\n  %s', command, i, line.strip())
        # print(f'set "{command}": "{content}"')
        quote = "'" if "'" not in content else '"'

        self.lines[i] = f'{line[:open_pos + 1]}{quote}{content}{quote}{end[1:]}'

    def _gather_new_imports(self):
        new_import_lines = []
        for mod, member_set in self.submods_used.items():
            member_names = sorted(member_set)
            line = f'from {PYSIDE_REPLACE}.{mod} import '

            rest = ', '.join(member_names)
            if len(line + rest) <= 95:
                new_import_lines.append(line + rest)
                continue

            line += '('
            for word in member_names[:-1]:
                if len(line + word) <= 95:
                    line += word + ', '
                    continue
                new_import_lines.append(line)
                line = '    ' + word + ', '
            line += member_names[-1] + ')'
            new_import_lines.append(line)
        return new_import_lines

    def _assemble_new_lines(self):
        new_lines = self.lines[: self.doc_block[0]]
        new_lines.append('"""\n')
        for i in range(self.doc_block[0] + 1, self.doc_block[1] - 1):
            line = self.lines[i].strip('# \n')
            if line:
                new_lines.append(line + '\n')
            else:
                new_lines.append('\n')
        new_lines.append('"""\n\n')

        new_import_lines = self._gather_new_imports()
        new_lines.append('\n'.join(new_import_lines) + '\n')
        # these are probably all other imports
        new_lines.extend(self.lines[self.imports_block[1] + 1: self.classes_start])
        # this skips all empty lines
        new_lines.extend(l for l in self.lines[self.classes_start:] if l)
        return new_lines


def _get_ui_basename_from_header(py_ui_path):
    """TODO: This is kinda ugly I don't think we need it."""
    uibase = None
    with open(py_ui_path, encoding='utf8') as fobj:
        line = fobj.readline()
        while line and uibase is not None:
            line = line.strip()
            if line.startswith('# Form implementation '):
                uibase = line[line.rfind("'", 0, -1) + 1 : -1]
                uibase = os.path.basename(uibase.strip())
                log.error('checkUiModule from read: %s', uibase)
                break
            line = fobj.readline()
    return uibase


def _get_qmembers():
    if QMEMBERS:
        return

    for mod in (QtCore, QtGui, QtWidgets, QtSvg):
        name = mod.__name__.split('.')[1]
        QMEMBERS[name] = [n for n in dir(mod) if not n.startswith('_') and n != PYSIDE_REPLACE]
        for member in QMEMBERS[name]:
            if member in MEMBERSQ:
                # print(f'{member} already listed in {MEMBERSQ[member]}!!')
                continue
            MEMBERSQ[member] = name


def _test():
    # import a2ui.a2design_ui
    # check_module(a2ui.a2design_ui, force=True)
    # import a2widget.a2hotkey.edit_func_widget_ui
    # check_module(a2widget.a2hotkey.edit_func_widget_ui, force=True)
    py_file_path = os.path.join(ROOT_PATH, r'ui\a2widget\a2hotkey\edit_func_widget_ui.py')
    ui_file_path = get_ui_file_path(py_file_path)
    call_uic(ui_file_path, py_file_path)
    UIPatcher(ui_file_path, py_file_path)


if __name__ == '__main__':
    _test()
